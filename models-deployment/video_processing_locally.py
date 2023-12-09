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

def process_video_locally(input_video_file_path, output_video_name="None", load_local_video=False):

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
    if output_video_name == "None":
        output_video = config['data']['output_video']
    else:
        output_video = output_video_name

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
    if load_local_video:
        # If load_local_video is True, use the local file path directly
        print(f"Loading local video: {input_video_file_path}")
        video_capture = cv2.VideoCapture(input_video_file_path)
    else:
        # If load_local_video is False, download the video from the URL
        print(f"Downloading video from URL: {input_video_file_path}")
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
            print(timestamp_str)
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
                    row_data["Box x"] = box[0]  # The YOLO model frames the object in a box, and x refers to the x-coordinate of the diagonal intersection (geometric center) of the box.
                    row_data["Box y"] = box[1]
                    row_data["Box width"] = box[2]
                    row_data["Box height"] = box[3]
                    row_data["Width-to-height ratio"] = box[2] / box[3]  # The width-to-height ratio of the box

                    # Append the data to the DataFrame
                    df_predict_data = pandas.concat([df_predict_data, pandas.DataFrame([row_data])],
                                                    ignore_index=True)
                    df_predict_data = df_predict_data.tail(1)
                    df_predict_data = df_predict_data.astype(float, errors='ignore')
                    df_predict_data.fillna(0, inplace=True)
                    new_column_order = ['Employee ID', 'Frame', 'Box x'] + [col for col in df_predict_data.columns if
                                                                            col not in ['Employee ID', 'Frame',
                                                                                        'Box x']]
                    df_predict_data = df_predict_data[new_column_order]
                    # print(df_predict_data.info())

                    try:
                        df_predict_data.drop(df_predict_data.columns[0], axis=1, inplace=True)
                        prediction = loaded_model.predict(df_predict_data)
                        prediction_probabilities = loaded_model.predict_proba(df_predict_data)
                        test_prob_df = pd.DataFrame(prediction_probabilities, columns=['non_fatigue', 'fatigue'])
                        fatigue_index_percent = round(test_prob_df.iloc[0]['fatigue'] * 100, 2)
                        # if prediction == 0:
                        #     prediction_result = 'Active'
                        # elif prediction == 1:
                        #     prediction_result = 'Fatigue'
                        # else:
                        #     prediction_result = 'Unknown'
                        if fatigue_index_percent <= 75:
                            prediction_result = 'Active'
                        elif fatigue_index_percent > 75:
                            prediction_result = 'Fatigue'
                        else:
                            prediction_result = 'Unknown'
                        prediction_results = [prediction_result, fatigue_index_percent]
                    except Exception as e:
                        print(f"An error occurred: {e}")
                        break
                    emp_id = "R{:03d}".format(person_idx + 101)
                    predict_data = {
                        'timestamp': timestamp_str,
                        'fatigue_status': prediction[0],
                        'emp_id': emp_id
                    }
                    df_predict_record = pandas.concat([df_predict_record, pandas.DataFrame([predict_data])],
                                                      ignore_index=True)

                    ### send message on websocket
                    index = prediction_results[1]
                    # print(timestamp_str, emp_id, index)
                    # insert_or_update_fatigue_history_index(db_connection, db_cursor, timestamp_str, emp_id, index)
                    # if (prediction[0] == 1):
                    #     insert_or_update_fatigue_history(db_connection, db_cursor, timestamp_str, emp_id)
                        # print(db_connection, db_cursor, timestamp_str, emp_id)
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
                        cv2.putText(frame, f"Status: ",(text_position[0],text_position[1] - 120), cv2.FONT_HERSHEY_SIMPLEX,
                                    0.75,
                                    (0, 0, 0) , 2)
                        cv2.putText(frame, f"   {prediction_result}",(text_position[0],text_position[1] - 85), cv2.FONT_HERSHEY_SIMPLEX,
                                    1,
                                    text_color, 2)
                        cv2.putText(frame, f"Index: ",(text_position[0],text_position[1] - 50), cv2.FONT_HERSHEY_SIMPLEX,
                                    0.75,
                                    (0, 0, 0) , 2)
                        cv2.putText(frame, f"   {fatigue_index_percent}",(text_position[0],text_position[1] - 15), cv2.FONT_HERSHEY_SIMPLEX,
                                    1,
                                    text_color, 2)
                        # Annotate bounding box details
                        # cv2.putText(frame, f"Box X: {box_x}", (text_position[0], text_position[1] - 120),
                        #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 2)
                        # cv2.putText(frame, f"Box Y: {box_y}", (text_position[0], text_position[1] - 90),
                        #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 2)
                        # cv2.putText(frame, f"Width: {box_w}", (text_position[0], text_position[1] - 60),
                        #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 2)
                        # cv2.putText(frame, f"Height: {box_h}", (text_position[0], text_position[1] - 30),
                        #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 2)
                        # width_to_height_ratio = box_w / box_h
                        # cv2.putText(frame, f"W/H Ratio: {width_to_height_ratio:.2f}",
                        #             (text_position[0], text_position[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        #             text_color, 2)

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


if __name__ == "__main__":
    process_video_locally('videos/input_videos/test_video.mp4', "videos/output_videos/test_video.mp4", load_local_video=True)
