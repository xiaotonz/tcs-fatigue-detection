import numpy as np
import requests
import cv2
from constants import KEYPOINT_LABELS, VIDEO_CHUNK_SIZE, FRAME_PROCESS_INTERVAL, UNKNOWN_EMPLOYEE, UNKNOWN_SHIFT

def download_video(video_url, video_file):
    # Using video_capture = download_video(video_url, video_file)
    response = requests.get(video_url, stream=True)
    if response.status_code == 200:
        with open(video_file, "wb") as video:
            for chunk in response.iter_content(chunk_size=VIDEO_CHUNK_SIZE):
                if chunk:
                    video.write(chunk)
        video_capture = cv2.VideoCapture(video_file)
        return video_capture
    else:
        print("Failed to parse the video. Status code:", response.status_code)
        return None

def calculate_and_get_angles_as_dict(adjacent_limbs, result_keypoint, limbs):
    angle_information = {}

    for limb_1_name, limb_2_name in adjacent_limbs:
        limb_1 = limbs[limb_1_name]
        limb_2 = limbs[limb_2_name]

        common_point = None
        for point in limb_1:
            if any(np.array_equal(point, p) for p in limb_2):
                common_point = point
                break

        if common_point is None:
            continue

        vector_A = np.array(limb_1[1]) - np.array(limb_1[0]) if np.array_equal(limb_1[1], common_point) else np.array(
            limb_1[0]) - np.array(limb_1[1])
        vector_B = np.array(limb_2[1]) - np.array(limb_2[0]) if np.array_equal(limb_2[1], common_point) else np.array(
            limb_2[0]) - np.array(limb_2[1])
        key_index = np.where((result_keypoint == common_point).all(axis=1))[0][0]
        key = f"{limb_1_name} - {KEYPOINT_LABELS[key_index]} - {limb_2_name}"

        if np.all(vector_A == 0) or np.all(vector_B == 0):
            angle = 180
        else:
            angle = calculate_angle(vector_A, vector_B)

        angle_information[key] = f"{angle:.1f}°"

    return angle_information

def find_closest_person_distance(prev_coordinates, current_coordinate):
    """
    Returns the index of the person from the previous frame whose coordinates
    are closest to the current_coordinate and the corresponding distance.
    """
    distances = [(idx, np.linalg.norm(np.array(prev_coord) - np.array(current_coordinate)))
                 for idx, prev_coord in enumerate(prev_coordinates) if prev_coord is not None]
    if distances:
        min_distance_item = min(distances, key=lambda x: x[1])
        return min_distance_item
    return None, float('inf')

def calculate_angle(A, B):
    # Calculate angle between two vectors A and B.
    dot_product = np.dot(A, B)
    norm_A = np.linalg.norm(A)
    norm_B = np.linalg.norm(B)

    cosine_angle = dot_product / (norm_A * norm_B)
    # Clip the cosine_angle to avoid out-of-range error
    cosine_angle = np.clip(cosine_angle, -1, 1)
    return np.arccos(cosine_angle) * (180 / np.pi)