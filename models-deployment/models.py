import pickle
from pydantic import BaseModel

def load_model(model_file_path):
    # Load the saved model from the file
    with open(model_file_path, "rb") as model_file:
        loaded_model = pickle.load(model_file)
    return loaded_model

class GetKeypoint(BaseModel):
    NOSE: int = 0
    LEFT_EYE: int = 1
    RIGHT_EYE: int = 2
    LEFT_EAR: int = 3
    RIGHT_EAR: int = 4
    LEFT_SHOULDER: int = 5
    RIGHT_SHOULDER: int = 6
    LEFT_ELBOW: int = 7
    RIGHT_ELBOW: int = 8
    LEFT_WRIST: int = 9
    RIGHT_WRIST: int = 10
    LEFT_HIP: int = 11
    RIGHT_HIP: int = 12
    LEFT_KNEE: int = 13
    RIGHT_KNEE: int = 14
    LEFT_ANKLE: int = 15
    RIGHT_ANKLE: int = 16


class BodyKeypoints:
    def __init__(self, keypoints):
        get_keypoint = GetKeypoint()
        self.NOSE = keypoints[get_keypoint.NOSE]
        self.LEFT_EYE = keypoints[get_keypoint.LEFT_EYE]
        self.RIGHT_EYE = keypoints[get_keypoint.RIGHT_EYE]
        self.LEFT_EAR = keypoints[get_keypoint.LEFT_EAR]
        self.RIGHT_EAR = keypoints[get_keypoint.RIGHT_EAR]
        self.LEFT_SHOULDER = keypoints[get_keypoint.LEFT_SHOULDER]
        self.RIGHT_SHOULDER = keypoints[get_keypoint.RIGHT_SHOULDER]
        self.LEFT_ELBOW = keypoints[get_keypoint.LEFT_ELBOW]
        self.RIGHT_ELBOW = keypoints[get_keypoint.RIGHT_ELBOW]
        self.LEFT_WRIST = keypoints[get_keypoint.LEFT_WRIST]
        self.RIGHT_WRIST = keypoints[get_keypoint.RIGHT_WRIST]
        self.LEFT_HIP = keypoints[get_keypoint.LEFT_HIP]
        self.RIGHT_HIP = keypoints[get_keypoint.RIGHT_HIP]
        self.LEFT_KNEE = keypoints[get_keypoint.LEFT_KNEE]
        self.RIGHT_KNEE = keypoints[get_keypoint.RIGHT_KNEE]
        self.LEFT_ANKLE = keypoints[get_keypoint.LEFT_ANKLE]
        self.RIGHT_ANKLE = keypoints[get_keypoint.RIGHT_ANKLE]


def get_limbs_from_keypoints(keypoints: BodyKeypoints):
    limbs = {
        "right_eye&nose": [keypoints.RIGHT_EYE, keypoints.NOSE],
        "right_eye&right_ear": [keypoints.RIGHT_EYE, keypoints.RIGHT_EAR],
        "left_eye&nose": [keypoints.LEFT_EYE, keypoints.NOSE],
        "left_eye&left_ear": [keypoints.LEFT_EYE, keypoints.LEFT_EAR],
        "right_shoulder&right_elbow": [keypoints.RIGHT_SHOULDER, keypoints.RIGHT_ELBOW],
        "right_elbow&right_wrist": [keypoints.RIGHT_ELBOW, keypoints.RIGHT_WRIST],
        "left_shoulder&left_elbow": [keypoints.LEFT_SHOULDER, keypoints.LEFT_ELBOW],
        "left_elbow&left_wrist": [keypoints.LEFT_ELBOW, keypoints.LEFT_WRIST],
        "right_hip&right_knee": [keypoints.RIGHT_HIP, keypoints.RIGHT_KNEE],
        "right_knee&right_ankle": [keypoints.RIGHT_KNEE, keypoints.RIGHT_ANKLE],
        "left_hip&left_knee": [keypoints.LEFT_HIP, keypoints.LEFT_KNEE],
        "left_knee&left_ankle": [keypoints.LEFT_KNEE, keypoints.LEFT_ANKLE],
        "right_shoulder&left_shoulder": [keypoints.RIGHT_SHOULDER, keypoints.LEFT_SHOULDER],
        "right_hip&left_hip": [keypoints.RIGHT_HIP, keypoints.LEFT_HIP],
        "right_shoulder&right_hip": [keypoints.RIGHT_SHOULDER, keypoints.RIGHT_HIP],
        "left_shoulder&left_hip": [keypoints.LEFT_SHOULDER, keypoints.LEFT_HIP]
    }
    return limbs