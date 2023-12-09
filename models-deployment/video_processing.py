from queue import Queue
from threading import Thread
# from websocket_message import start_server, send_message
import asyncio
from fastapi import FastAPI, WebSocket, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import json
import os
import cv2
# from flask import Flask, request, jsonify
import pandas
import pandas as pd
import tqdm
from joblib import load
import uuid
from ultralytics import YOLO
from datetime import datetime, timedelta
from config import read_config
from constants import ANGLE_KEYS, SELECTED_LIMBS, DATAFRAME_PREDICT_COLUMNS, PREDICT_RECORD_COLUMNS, NNPACK_MODE, \
    DATE_FORMAT, DEFAULT_TIME
from models import load_model, GetKeypoint, BodyKeypoints, get_limbs_from_keypoints
from utils import download_video, calculate_and_get_angles_as_dict, find_closest_person_distance
from database import initialize_database, insert_or_update_fatigue_history, insert_or_update_fatigue_history_index


# app = Flask(__name__)
app = FastAPI()

html = """
<!DOCTYPE html>
<html>
        <script>
            var ws1 = new WebSocket("ws://localhost:8000/ws1");
            var ws2 = new WebSocket("ws://localhost:8000/ws2");
        </script>
</html>
"""


tasks = {}
task_queue = Queue()


message_queue_e1 = []
message_queue_e2 = []

class Task(BaseModel):
    url: str

def worker():
    while True:
        task_id, input_video_file_path = task_queue.get()
        process_video(input_video_file_path, task_id)
        task_queue.task_done()

thread = Thread(target=worker)
thread.daemon = True
thread.start()

@app.get("/")
async def get():
    return HTMLResponse(html)

@app.get("/process")
async def process_video_endpoint(request: Request):
    url = request.query_params.get("url")

    input_video_file_path = url
    if not input_video_file_path:
        raise HTTPException(status_code=400, detail="Video URL not provided")
    task_id = str(uuid.uuid4())
    # Store both the status and the URL with the task
    tasks[task_id] = {'status': 'Processing', 'url': input_video_file_path}
    # Queue the video processing task for background execution here
    task_queue.put((task_id, input_video_file_path))
    return {'message': 'Video is being processed', 'task_id': task_id}

@app.get("/status/{task_id}")
async def get_status(task_id: str):
    # Get the task information by ID
    task = tasks.get(task_id)
    if task:
        # Return the status and the original video URL
        return {'task_id': task_id, 'status': task['status'], 'video_url': task['url']}
    else:
        # Default message if the task does not exist
        raise HTTPException(status_code=404, detail="No such task")

@app.get("/tasks")
async def get_all_tasks():
    return tasks

def update_task_status(task_id: str, status: str):
    if task_id in tasks:
        tasks[task_id]['status'] = status

def process_video(input_video_file_path, task_id):
    try:
        # Set environment variable for NNPACK
        os.environ["NNPACK_MODE"] = NNPACK_MODE

        # Load the configuration file
        config = read_config('config.ini')

        # Set model variable
        yolo_model = config['model']['yolo_model']
        # file_path = config['model']['xgboost_model']
        file_path = config['model']['body_joint_rf_model']
        interval_frame = int(config['model']['interval_frame'])

        # Set data variable
        video_file = config['data']['video_file']
        output_video = config['data']['output_video']

        # default_label = config['data']['default_label']

        video_url = config['data']['video_url'].strip('"')

        prev_person_coordinates = [None, None]

        # Set DB variable
        db_connection, db_cursor = initialize_database(config)

        df_predict_data = pd.DataFrame(columns=DATAFRAME_PREDICT_COLUMNS)
        df_predict_record = pd.DataFrame(columns=PREDICT_RECORD_COLUMNS)

        if input_video_file_path is None:
            # If the function parameter is not set, fall back to the default video file path from the configuration
            input_video_file_path = video_url
        else:
            print(f"Received URL: {input_video_file_path}")

        # Load models
        model = YOLO(yolo_model)
        loaded_model = load(file_path)

        # Open the test video file
        video_capture = download_video(input_video_file_path, video_file)

        # Get the dimensions of the video frame
        frame_width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = video_capture.get(cv2.CAP_PROP_FPS)

        skip_frames = int(interval_frame)
        total_processed_frames = int(total_frames / (skip_frames + 1))

        progress_bar = tqdm.tqdm(total=total_processed_frames, desc="Processing", unit="frame")

        frame_count = 0
        processed_frame_count = 0

        # Create a VideoWriter object to save the annotated video
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        output_video = cv2.VideoWriter(output_video, fourcc, fps, (frame_width, frame_height))

        limbs = get_limbs_from_keypoints(BodyKeypoints([[0, 0]] * 17))

        adjacent_limbs = []

        # Generating all possible combinations
        for i in range(len(SELECTED_LIMBS)):
            for j in range(i + 1, len(SELECTED_LIMBS)):
                limb1 = limbs[SELECTED_LIMBS[i]]
                limb2 = limbs[SELECTED_LIMBS[j]]

                # Convert keypoints to tuples for comparison
                limb1_tuples = [tuple(point) for point in limb1]
                limb2_tuples = [tuple(point) for point in limb2]

                # Checking if any keypoint in the second limb matches with the keypoints in the first limb
                if any(kp in limb1_tuples for kp in limb2_tuples):
                    adjacent_limbs.append((SELECTED_LIMBS[i], SELECTED_LIMBS[j]))
        # start_time = datetime.strptime(DEFAULT_TIME, DATE_FORMAT)
        start_time = datetime.now()

        while True:
            ret, frame = video_capture.read()

            if not ret:
                break

            if frame_count % (skip_frames + 1) == 0:
                current_time = start_time + timedelta(seconds=(processed_frame_count * (skip_frames + 1)) / fps)
                timestamp_str = current_time.strftime(DATE_FORMAT)[:-3]
                # Process the frame with the YOLO model to get the keypoints and bounding boxes
                results = model.predict(frame, save=False, conf=0.5)

                # Iterate through results to get bounding boxes and keypoints data
                for idx, result in enumerate(results):
                    keypoints_data = result.keypoints.xy.cpu().numpy() if hasattr(result, 'keypoints') else []
                    boxes_data = result.boxes.xywh.cpu().numpy() if hasattr(result,
                                                                            'boxes') else []  # Extract bounding boxes

                    distances_and_indices = []

                    # For each person, get the keypoints and determine which "employee" they match based on the nose's position
                    for person_idx, result_keypoint in enumerate(keypoints_data):
                        if len(result_keypoint) == 0:
                            continue
                        get_keypoint = GetKeypoint()
                        nose_coordinate = tuple(result_keypoint[get_keypoint.NOSE])
                        matched_person_idx, distance = find_closest_person_distance(prev_person_coordinates,
                                                                                    nose_coordinate)
                        distances_and_indices.append((distance, matched_person_idx, person_idx, result_keypoint))

                    sorted_matches = sorted(distances_and_indices, key=lambda x: x[0])[:2]

                    for distance, matched_person_idx, person_idx, result_keypoint in sorted_matches:
                        if matched_person_idx is not None:
                            prev_person_coordinates[matched_person_idx] = tuple(result_keypoint[get_keypoint.NOSE])

                        body_keypoints = BodyKeypoints(result_keypoint)
                        limbs = get_limbs_from_keypoints(body_keypoints)
                        angle_info_dict = calculate_and_get_angles_as_dict(adjacent_limbs, result_keypoint, limbs)
                        # Construct the row data to be appended to the DataFrame
                        row_data = {
                            "Employee ID": person_idx + 1,
                            "Frame": processed_frame_count,
                        }
                        #         for label, keypoint in zip(KEYPOINT_LABELS, result_keypoint):
                        #             row_data[f"{label} (x, y)"] = tuple(keypoint)
                        for angle_key in ANGLE_KEYS:
                            angle_value = angle_info_dict.get(angle_key, None)
                            if angle_value:
                                angle_value = ''.join([char for char in angle_value if char.isdigit() or char == '.'])
                            row_data[angle_key] = angle_value

                        # Include bounding box data for this person
                        box = boxes_data[person_idx] if len(boxes_data) > person_idx else [None, None, None, None]
                        # row_data["Bounding Box (x, y, w, h)"] = tuple(box)
                        row_data["Box x"] = box[
                            0]  # The YOLO model frames the object in a box, and x refers to the x-coordinate of the diagonal intersection (geometric center) of the box.
                        row_data["Box y"] = box[1]
                        row_data["Box width"] = box[2]
                        row_data["Box height"] = box[3]
                        row_data["Width-to-height ratio"] = box[2] / box[3]  # The width-to-height ratio of the box

                        # Append the data to the DataFrame
                        df_predict_data = pandas.concat([df_predict_data, pandas.DataFrame([row_data])], ignore_index=True)
                        df_predict_data = df_predict_data.tail(1)
                        df_predict_data = df_predict_data.astype(float, errors='ignore')
                        df_predict_data.fillna(0, inplace=True)
                        new_column_order = ['Employee ID', 'Frame', 'Box x'] + [col for col in df_predict_data.columns
                                                                                if
                                                                                col not in ['Employee ID', 'Frame',
                                                                                            'Box x']]
                        df_predict_data = df_predict_data[new_column_order]
                        try:
                            df_predict_data.drop(df_predict_data.columns[0], axis=1, inplace=True)
                            prediction = loaded_model.predict(df_predict_data)
                            prediction_probabilities = loaded_model.predict_proba(df_predict_data)
                            test_prob_df = pd.DataFrame(prediction_probabilities, columns=['non_fatigue', 'fatigue'])
                            fatigue_index_percent = round(test_prob_df.iloc[0]['fatigue'] * 100, 2)
                            if prediction == 0:
                                prediction_result = 'Active'
                            elif prediction == 1:
                                prediction_result = 'Fatigue'
                            else:
                                prediction_result = 'Unknown'
                            prediction_results = [prediction_result, fatigue_index_percent]
                        except Exception as e:
                            print(f"An error occurred: {e}")
                            break
                        emp_id = "E{:03d}".format(person_idx + 101)
                        predict_data = {
                            'timestamp': timestamp_str,
                            'fatigue_status': prediction[0],
                            'emp_id': emp_id
                        }
                        df_predict_record = pandas.concat([df_predict_record, pandas.DataFrame([predict_data])],
                                                        ignore_index=True)

                        

                        ### send message on websocket
                        index = prediction_results[1]
                        insert_or_update_fatigue_history_index(db_connection, db_cursor, timestamp_str, emp_id, index)
                        message_data = {
                            "timestamp": timestamp_str,
                            "employee_id": emp_id,
                            "index": index
                        }
                        json_message = json.dumps(message_data)

                        if message_data['employee_id'] == 'E101':
                            message_queue_e1.append(json_message)
                            
                        if message_data['employee_id'] == 'E102':
                            message_queue_e2.append(json_message)

                        # message_queue.append(timestamp_str + '~' + emp_id + '~' + index)
                        
                        if(index>0.5):
                            insert_or_update_fatigue_history(db_connection, db_cursor, timestamp_str, emp_id)

                        #     send_message(timestamp_str+'~'+emp_id)


                        if all(box):  # Check if bounding box data was obtained
                            box_x, box_y, box_w, box_h = box
                            top_left = (int(box_x - box_w / 2),
                                        int(box_y - box_h / 2))  # Calculate the coordinates of the top left corner of the bounding box
                            bottom_right = (int(box_x + box_w / 2),
                                            int(box_y + box_h / 2))  # Calculate the coordinates of the bottom right corner of the bounding box

                            # Draw the bounding box
                            cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0),
                                          2)  # Draw bounding box with green color lines

                            # Draw the prediction text
                            text_position = (top_left[0], top_left[
                                1] - 10)  # Calculate the position of the text so it appears above the bounding box
                            # Choose text color based on prediction result
                            if prediction_result == 'Active':
                                text_color = (0, 255, 0)  # Green color
                            else:
                                text_color = (0, 0, 255)  # Red color
                            cv2.putText(frame, f"Status: {prediction_result}", text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                        text_color, 2)

                # Write the annotated frame to the output video
                processed_frame_count += 1
                progress_bar.update(1)
                for _ in range(skip_frames + 1):
                    output_video.write(frame)
            frame_count += 1

        # Release the video capture and writer
        print(df_predict_record)
        video_capture.release()
        output_video.release()
        cv2.destroyAllWindows()
        update_task_status(task_id, 'Finished')
    except Exception as e:
        update_task_status(task_id, f'Error: {str(e)}')

# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=80)

@app.websocket("/ws1")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        await send_messages(websocket, message_queue_e1)  # Start sending messages in background

  
    except Exception as e:
        print("WebSocket error:", e) 

@app.websocket("/ws2")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        await send_messages(websocket, message_queue_e2)  # Start sending messages in background

  
    except Exception as e:
        print("WebSocket error:", e) 

async def send_messages(websocket: WebSocket, message_queue: list):
    while True:
        if message_queue:
            message = message_queue.pop(0)  # Dequeue message
            await websocket.send_json(
                {
                    "message": message
                }
            )  # Send message through WebSocket
        
        await asyncio.sleep(1)  # Adjust sleep duration as needed

    # process_video("https://tcsfatiguemlen1658192275.blob.core.windows.net/asset-505652fb-70d9-4bf1-8df7-bc33f6a5f000/test_video%%20(1).mp4")
