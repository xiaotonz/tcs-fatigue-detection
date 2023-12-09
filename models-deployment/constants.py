# constants.py
NNPACK_MODE = "NATIVE"
VIDEO_CHUNK_SIZE = 1024
FRAME_PROCESS_INTERVAL = 5
UNKNOWN_EMPLOYEE = "Unknown"
UNKNOWN_SHIFT = -1
DATE_FORMAT = '%Y-%m-%d %H:%M:%S.%f'
EMPLOYEE_ID = "Employee ID"
FRAME = "Frame"
BOX_X = "Box x"
BOX_Y = "Box y"
BOX_WIDTH = "Box width"
BOX_HEIGHT = "Box height"
WIDTH_TO_HEIGHT_RATIO = "Width-to-height ratio"
FATIGUE_STATUS = "Fatigue or not"
DEFAULT_TIME = '2023-01-01 00:00:00.000000'

KEYPOINT_LABELS = [
    "NOSE", "LEFT_EYE", "RIGHT_EYE", "LEFT_EAR", "RIGHT_EAR", "LEFT_SHOULDER",
    "RIGHT_SHOULDER", "LEFT_ELBOW", "RIGHT_ELBOW", "LEFT_WRIST", "RIGHT_WRIST",
    "LEFT_HIP", "RIGHT_HIP", "LEFT_KNEE", "RIGHT_KNEE", "LEFT_ANKLE", "RIGHT_ANKLE"
]
ANGLE_KEYS = [
    'right_shoulder&right_elbow - RIGHT_ELBOW - right_elbow&right_wrist',
    'right_shoulder&right_elbow - RIGHT_SHOULDER - right_shoulder&left_shoulder',
    'right_shoulder&right_elbow - RIGHT_SHOULDER - right_shoulder&right_hip',
    'left_shoulder&left_elbow - LEFT_ELBOW - left_elbow&left_wrist',
    'left_shoulder&left_elbow - LEFT_SHOULDER - right_shoulder&left_shoulder',
    'left_shoulder&left_elbow - LEFT_SHOULDER - left_shoulder&left_hip',
    'right_hip&right_knee - RIGHT_KNEE - right_knee&right_ankle',
    'right_hip&right_knee - RIGHT_HIP - right_hip&left_hip',
    'right_hip&right_knee - RIGHT_HIP - right_shoulder&right_hip',
    'left_hip&left_knee - LEFT_KNEE - left_knee&left_ankle',
    'left_hip&left_knee - LEFT_HIP - right_hip&left_hip',
    'left_hip&left_knee - LEFT_HIP - left_shoulder&left_hip',
    'right_shoulder&left_shoulder - RIGHT_SHOULDER - right_shoulder&right_hip',
    'right_shoulder&left_shoulder - LEFT_SHOULDER - left_shoulder&left_hip',
    'right_hip&left_hip - RIGHT_HIP - right_shoulder&right_hip',
    'right_hip&left_hip - LEFT_HIP - left_shoulder&left_hip'
]
SELECTED_LIMBS = [
        "right_shoulder&right_elbow",
        "right_elbow&right_wrist",
        "left_shoulder&left_elbow",
        "left_elbow&left_wrist",
        "right_hip&right_knee",
        "right_knee&right_ankle",
        "left_hip&left_knee",
        "left_knee&left_ankle",
        "right_shoulder&left_shoulder",
        "right_hip&left_hip",
        "right_shoulder&right_hip",
        "left_shoulder&left_hip"
    ]

DATAFRAME_PREDICT_COLUMNS = [EMPLOYEE_ID, FRAME, BOX_X, BOX_Y, BOX_WIDTH, BOX_HEIGHT, WIDTH_TO_HEIGHT_RATIO] + ANGLE_KEYS

PREDICT_RECORD_COLUMNS = ["emp_id", "timestamp", "fatigue_status"]