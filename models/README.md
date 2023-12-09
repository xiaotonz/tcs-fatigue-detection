# Converting Video or Image into Angle Data

<h6 style="text-align:right">Edited: SEP 27, 2023</h1>
<h6 style="text-align:right">Version: 1.0 </h1>


## I. Overview

This document provides a guide on detecting and extracting body joint from a video or image, and subsequently calculating the angles between various body limbs.



## II. Prerequisites

YOLO-Pose (YOLOv8n-pose): Pose detection model

![image-20231010173911758](https://p.ipic.vip/dtso0n.png)



## III. Detecting and Extracting Keypoints from Video or Image

The YOLO-Pose model processes images or videos and labels them with pose positions. In addition to producing a image marked with human joints or limbs, there's keypoints data generated for every frame, which might be helpful for our fatigue detection. 

Keypoints are the primary output for human joints detection, containing coordinates of 17 human keypoints (like arm, head, etc.) in the image.

```python
import numpy as np
from ultralytics import YOLO

model = YOLO('yolov8n-pose.pt')
img = '1.jpg'
results = model(img)
result_keypoint = results[0].keypoints.xy.cpu().numpy()[0]
```

Use a pre-trained pose estimation model to detect body keypoints. This will provide a set of (x, y) coordinates for each keypoint detected in the image or each frame of the video.

Example output:

```json
[[     258.57      236.97]
 [     275.37      208.16]
 [     248.45       218.4]
 [     343.27      186.25]
 [     265.84      215.34]
 [     475.76      290.51]
 [     286.95      325.27]
 [     588.49      458.98]
 [      272.7         477]
 [     450.04       598.2]
 [     180.71      578.69]
 [     458.07      648.46]
 [     331.24      643.85]
 [     461.05      913.61]
 [     276.25      894.53]
 [     489.96      1169.2]
 [     280.05      1141.1]]
```

Can aslo using `results[0].keypoints.xyn.cpu().numpy()[0]` to get normalized data:

```json
// Normalization
[[    0.36164     0.17764]
 [    0.38513     0.15605]
 [    0.34749     0.16372]
 [     0.4801     0.13962]
 [    0.37181     0.16142]
 [     0.6654     0.21777]
 [    0.40133     0.24383]
 [    0.82306     0.34406]
 [    0.38141     0.35757]
 [    0.62942     0.44842]
 [    0.25275      0.4338]
 [    0.64065      0.4861]
 [    0.46327     0.48264]
 [    0.64482     0.68486]
 [    0.38636     0.67056]
 [    0.68526     0.87647]
 [    0.39168      0.8554]]
```



## IV. Calculate the Angles between Joints

### 1. Define Body Parts

**Map each keypoint to specific body parts such as the Left-shoulder, Left-elbow, Left-knee, etc.**

##### i. YOLO-Pose labeled 14 positions of the body

```json
KEYPOINT_LABELS = [
    "NOSE", "LEFT_EYE", "RIGHT_EYE", "LEFT_EAR", "RIGHT_EAR", "LEFT_SHOULDER",
    "RIGHT_SHOULDER", "LEFT_ELBOW", "RIGHT_ELBOW", "LEFT_WRIST", "RIGHT_WRIST",
    "LEFT_HIP", "RIGHT_HIP", "LEFT_KNEE", "RIGHT_KNEE", "LEFT_ANKLE", "RIGHT_ANKLE"
]
```

##### ii. The points are labeled and plotted using the `matplotlib.pyplot` library, labeling each point with the limb or joint it represents.

![image-20230926222254528](https://p.ipic.vip/mjsfrp.png)

```python
from pydantic import BaseModel
from ultralytics import YOLO

class GetKeypoint(BaseModel):
    NOSE:           int = 0
    LEFT_EYE:       int = 1
    RIGHT_EYE:      int = 2
    LEFT_EAR:       int = 3
    RIGHT_EAR:      int = 4
    LEFT_SHOULDER:  int = 5
    RIGHT_SHOULDER: int = 6
    LEFT_ELBOW:     int = 7
    RIGHT_ELBOW:    int = 8
    LEFT_WRIST:     int = 9
    RIGHT_WRIST:    int = 10
    LEFT_HIP:       int = 11
    RIGHT_HIP:      int = 12
    LEFT_KNEE:      int = 13
    RIGHT_KNEE:     int = 14
    LEFT_ANKLE:     int = 15
    RIGHT_ANKLE:    int = 16

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
        
model = YOLO('yolov8n-pose.pt')
img = 'frame_1.jpg'
results = model(img)
result_keypoint = results[0].keypoints.xyn.cpu().numpy()[0]

get_keypoint = GetKeypoint()
nose_x, nose_y = result_keypoint[get_keypoint.NOSE]
left_eye_x, left_eye_y = result_keypoint[get_keypoint.LEFT_EYE]
print(nose_x, nose_y)
```

##### iii. Result (labeling each point with the limb or joint):

![image-20231010231146287](https://p.ipic.vip/mzvi8z.png)

| Index | Key point      |
| ----- | -------------- |
| 1     | Nose           |
| 2     | Left-eye       |
| 3     | Right-eye      |
| 4     | Left-ear       |
| 5     | Right-ear      |
| 6     | Left-shoulder  |
| 7     | Right-shoulder |
| 8     | Left-elbow     |
| 9     | Right-elbow    |
| 10    | Left-wrist     |
| 11    | Right-wrist    |
| 12    | Left-hip       |
| 13    | Right-hip      |
| 14    | Left-knee      |
| 15    | Right-knee     |
| 16    | Left-ankle     |
| 17    | Right-ankle    |



### 2. Mark the limbs represented by each point in the "Pose".

##### i. Define limbs or joint as line segments connecting two keypoints. For instance, the line segment connecting the right shoulder keypoint and right elbow keypoint is a limb.

![image-20230926192858337](https://p.ipic.vip/cdff8b.png)



##### ii. Mark each line in the "Pose".

```python
def get_limbs_from_keypoints(keypoints: BodyKeypoints):
    limbs = {
        "right_eye-nose": [keypoints.RIGHT_EYE, keypoints.NOSE],
        "right_eye-right_ear": [keypoints.RIGHT_EYE, keypoints.RIGHT_EAR],
        "left_eye-nose": [keypoints.LEFT_EYE, keypoints.NOSE],
        "left_eye-left_ear": [keypoints.LEFT_EYE, keypoints.LEFT_EAR],
        "right_shoulder-right_elbow": [keypoints.RIGHT_SHOULDER, keypoints.RIGHT_ELBOW],
        "right_elbow-right_wrist": [keypoints.RIGHT_ELBOW, keypoints.RIGHT_WRIST],
        "left_shoulder-left_elbow": [keypoints.LEFT_SHOULDER, keypoints.LEFT_ELBOW],
        "left_elbow-left_wrist": [keypoints.LEFT_ELBOW, keypoints.LEFT_WRIST],
        "right_hip-right_knee": [keypoints.RIGHT_HIP, keypoints.RIGHT_KNEE],
        "right_knee-right_ankle": [keypoints.RIGHT_KNEE, keypoints.RIGHT_ANKLE],
        "left_hip-left_knee": [keypoints.LEFT_HIP, keypoints.LEFT_KNEE],
        "left_knee-left_ankle": [keypoints.LEFT_KNEE, keypoints.LEFT_ANKLE],
        "right_shoulder-left_shoulder": [keypoints.RIGHT_SHOULDER, keypoints.LEFT_SHOULDER],
        "right_hip-left_hip": [keypoints.RIGHT_HIP, keypoints.LEFT_HIP],
        "right_shoulder-right_hip": [keypoints.RIGHT_SHOULDER, keypoints.RIGHT_HIP],
        "left_shoulder-left_hip": [keypoints.LEFT_SHOULDER, keypoints.LEFT_HIP]
    }
    return limbs
   
def plot_keypoints_with_multiple_datasets(keypoints_datasets, limbs_template):
        # Draw lines and add labels
        for limb_name, limb in limbs.items():
            x_values = [limb[0][0], limb[1][0]]
            y_values = [limb[0][1], limb[1][1]]
            plt.plot(x_values, y_values, 'r-')

            mid_x = sum(x_values) / 2
            mid_y = sum(y_values) / 2
            offset = 0.02
            indicator_end_x = mid_x + offset
            indicator_end_y = mid_y + offset
            plt.plot([mid_x, indicator_end_x], [mid_y, indicator_end_y], '--', color=INDICATOR_LINE_COLOR)
            plt.annotate(limb_name, (indicator_end_x, indicator_end_y), fontsize=8, ha='right', color=LINE_LABEL_COLOR)
```

##### iii. Result(Mark each limb line)

![image-20230926222712711](https://p.ipic.vip/qpz57h.png)

### 3. Calculating Joint Angles Between Body Parts

##### i. Calculation Joint Angle Principle

For each pair of adjacent limbs, calculate the joint angle between them using the dot product and the norms of the vectors representing the limbs:

![image-20230926222840887](https://p.ipic.vip/s4fho2.png)

```python
def calculate_angle(A, B):
    dot_product = np.dot(A, B)
    norm_A = np.linalg.norm(A)
    norm_B = np.linalg.norm(B)
    return np.arccos(dot_product / (norm_A * norm_B)) * (180/np.pi)
 
def plot_keypoints_with_multiple_datasets(keypoints_datasets, limbs_template):
        # Calculate and annotate angles for adjacent limbs
        for limb_1_name, limb_2_name in adjacent_limbs:
            limb_1 = limbs[limb_1_name]
            limb_2 = limbs[limb_2_name]
            
            common_point = None
            for point in limb_1:
                if any(np.array_equal(point, p) for p in limb_2):
                    common_point = np.array(point)
                    break

            if common_point is None:
                continue

            # Get vector A and B
            vector_A = np.array(limb_1[1]) - np.array(limb_1[0]) if np.array_equal(limb_1[1], common_point) else np.array(limb_1[0]) - np.array(limb_1[1])
            vector_B = np.array(limb_2[1]) - np.array(limb_2[0]) if np.array_equal(limb_2[1], common_point) else np.array(limb_2[0]) - np.array(limb_2[1])

            angle = calculate_angle(vector_A, vector_B)

            # Determine the offset for multiple angles at the same point
            if common_point.tobytes() not in angle_offsets:
                angle_offsets[common_point.tobytes()] = 0
            else:
                angle_offsets[common_point.tobytes()] += 1

            offset_angle = OFFSET_ANGLES[angle_offsets[common_point.tobytes()] % len(OFFSET_ANGLES)]
            offset_dx = 50 * np.cos(np.radians(offset_angle))
            offset_dy = 50 * np.sin(np.radians(offset_angle))

            end_point = common_point + np.array([offset_dx, offset_dy])

            plt.plot([common_point[0], end_point[0]], [common_point[1], end_point[1]], linestyle='--', color=ANGLE_INDICATOR_LINE_COLOR)
            plt.annotate(f"{angle:.1f}°", end_point, fontsize=8, ha='center', va='center', color=ANGLE_LABEL_COLOR)
```

##### ii. Result (image marked joint angle data)

![image-20230926222956907](https://p.ipic.vip/ah9mqg.png)

##### iii.Save angle joint data as a dict:

```python
def calculate_and_get_angles_as_dict(keypoints_coords, limbs):
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
        
        vector_A = np.array(limb_1[1]) - np.array(limb_1[0]) if np.array_equal(limb_1[1], common_point) else np.array(limb_1[0]) - np.array(limb_1[1])
        vector_B = np.array(limb_2[1]) - np.array(limb_2[0]) if np.array_equal(limb_2[1], common_point) else np.array(limb_2[0]) - np.array(limb_2[1])
        
        angle = calculate_angle(vector_A, vector_B)
        key = f"{limb_1_name} - {KEYPOINT_LABELS[np.where((result_keypoint == common_point).all(axis=1))[0][0]]} - {limb_2_name}"
        value = f"{angle:.1f}°"
        
        angle_information[key] = value
        
    return angle_information

angle_info_dict = calculate_and_get_angles_as_dict(result_keypoint, limbs)
angle_info_dict
```

##### iv. Result (saved joint angle data sample):

```json
{'right_shoulder&right_elbow - RIGHT_ELBOW - right_elbow&right_wrist': '143.2°',
 'right_shoulder&right_elbow - RIGHT_SHOULDER - right_shoulder&left_shoulder': '105.8°',
 'right_shoulder&right_elbow - RIGHT_SHOULDER - right_shoulder&right_hip': '13.3°',
 'left_shoulder&left_elbow - LEFT_ELBOW - left_elbow&left_wrist': '101.4°',
 'left_shoulder&left_elbow - LEFT_SHOULDER - right_shoulder&left_shoulder': '113.4°',
 'left_shoulder&left_elbow - LEFT_SHOULDER - left_shoulder&left_hip': '36.6°',
 'right_hip&right_knee - RIGHT_KNEE - right_knee&right_ankle': '166.7°',
 'right_hip&right_knee - RIGHT_HIP - right_hip&left_hip': '100.3°',
 'right_hip&right_knee - RIGHT_HIP - right_shoulder&right_hip': '159.7°',
 'left_hip&left_knee - LEFT_KNEE - left_knee&left_ankle': '174.2°',
 'left_hip&left_knee - LEFT_HIP - right_hip&left_hip': '92.7°',
 'left_hip&left_knee - LEFT_HIP - left_shoulder&left_hip': '176.5°',
 'right_shoulder&left_shoulder - RIGHT_SHOULDER - right_shoulder&right_hip': '92.5°',
 'right_shoulder&left_shoulder - LEFT_SHOULDER - left_shoulder&left_hip': '76.7°',
 'right_hip&left_hip - RIGHT_HIP - right_shoulder&right_hip': '100.0°',
 'right_hip&left_hip - LEFT_HIP - left_shoulder&left_hip': '90.7°'}
```



## V. Output the information of two workers

### 1. Image Input:

![frame_1](https://p.ipic.vip/kfo6k0.jpg)

### 2. Image Output:

![image-20230927100358026](https://p.ipic.vip/mjn1nv.png)

### 3. Angle info output

```json
[[     857.92      426.84]
 [     859.38      419.51]
 [     856.43      419.34]
 [     839.77      411.42]
 [     842.07      411.98]
 [     813.18      424.45]
 [     810.29      428.67]
 [     817.46      476.68]
 [     799.08      484.87]
 [      839.9      512.36]
 [     820.72      517.18]
 [     759.75      496.95]
 [     756.39      500.26]
 [     801.75      580.06]
 [     798.33      584.02]
 [      782.6      664.82]
 [     777.11      674.51]]
{'right_shoulder&right_elbow - RIGHT_ELBOW - right_elbow&right_wrist': '134.9°', 'right_shoulder&right_elbow - RIGHT_SHOULDER - right_shoulder&left_shoulder': '156.9°', 'right_shoulder&right_elbow - RIGHT_SHOULDER - right_shoulder&right_hip': '25.7°', 'left_shoulder&left_elbow - LEFT_ELBOW - left_elbow&left_wrist': '152.5°', 'left_shoulder&left_elbow - LEFT_SHOULDER - right_shoulder&left_shoulder': '39.1°', 'left_shoulder&left_elbow - LEFT_SHOULDER - left_shoulder&left_hip': '41.1°', 'right_hip&right_knee - RIGHT_KNEE - right_knee&right_ankle': '140.2°', 'right_hip&right_knee - RIGHT_HIP - right_hip&left_hip': '107.9°', 'right_hip&right_knee - RIGHT_HIP - right_shoulder&right_hip': '116.4°', 'left_hip&left_knee - LEFT_KNEE - left_knee&left_ankle': '140.5°', 'left_hip&left_knee - LEFT_HIP - right_hip&left_hip': '72.3°', 'left_hip&left_knee - LEFT_HIP - left_shoulder&left_hip': '116.8°', 'right_shoulder&left_shoulder - RIGHT_SHOULDER - right_shoulder&right_hip': '177.4°', 'right_shoulder&left_shoulder - LEFT_SHOULDER - left_shoulder&left_hip': '2.0°', 'right_hip&left_hip - RIGHT_HIP - right_shoulder&right_hip': '8.5°', 'right_hip&left_hip - LEFT_HIP - left_shoulder&left_hip': '170.9°'}
[[     979.62      400.33]
 [     981.39      392.15]
 [     978.28      392.52]
 [     994.79      382.84]
 [     998.82      381.91]
 [     1016.6      404.61]
 [     1029.7      399.33]
 [     1020.5       464.8]
 [     1039.5       456.1]
 [     1000.7      513.28]
 [     1012.2      505.32]
 [     1056.7      495.63]
 [     1066.5      492.07]
 [     1028.6      578.29]
 [     1043.8      574.43]
 [     1043.5      663.21]
 [       1058      653.31]]
{'right_shoulder&right_elbow - RIGHT_ELBOW - right_elbow&right_wrist': '141.1°', 'right_shoulder&right_elbow - RIGHT_SHOULDER - right_shoulder&left_shoulder': '78.0°', 'right_shoulder&right_elbow - RIGHT_SHOULDER - right_shoulder&right_hip': '11.9°', 'left_shoulder&left_elbow - LEFT_ELBOW - left_elbow&left_wrist': '154.0°', 'left_shoulder&left_elbow - LEFT_SHOULDER - right_shoulder&left_shoulder': '108.1°', 'left_shoulder&left_elbow - LEFT_SHOULDER - left_shoulder&left_hip': '20.1°', 'right_hip&right_knee - RIGHT_KNEE - right_knee&right_ankle': '154.3°', 'right_hip&right_knee - RIGHT_HIP - right_hip&left_hip': '54.6°', 'right_hip&right_knee - RIGHT_HIP - right_shoulder&right_hip': '142.9°', 'left_hip&left_knee - LEFT_KNEE - left_knee&left_ankle': '151.3°', 'left_hip&left_knee - LEFT_HIP - right_hip&left_hip': '128.7°', 'left_hip&left_knee - LEFT_HIP - left_shoulder&left_hip': '137.4°', 'right_shoulder&left_shoulder - RIGHT_SHOULDER - right_shoulder&right_hip': '89.8°', 'right_shoulder&left_shoulder - LEFT_SHOULDER - left_shoulder&left_hip': '88.0°', 'right_hip&left_hip - RIGHT_HIP - right_shoulder&right_hip': '88.3°', 'right_hip&left_hip - LEFT_HIP - left_shoulder&left_hip': '93.9°'}
```

I'm trying to store this information in tables, but the choice of which data to store, and the specific structure and format need to be further discussed by the team.

### 4. Table

 Exported all the data and put it in a dataframe:

```python
for idx in range(len(results)):
    keypoints_data = results[idx].keypoints.xy.cpu().numpy()
    
    for person_idx, result_keypoint in enumerate(keypoints_data):
        body_keypoints = BodyKeypoints(result_keypoint)
        limbs = get_limbs_from_keypoints(body_keypoints)
        angle_info_dict = calculate_and_get_angles_as_dict(result_keypoint, limbs)

        # Create a dictionary for the row data
        row_data = {
            "Employee ID": person_idx + 1,  #"Employee ID" = person_idx + 1
            "Frame": idx + 1,
        }
        for label, keypoint in zip(KEYPOINT_LABELS, result_keypoint):
            row_data[f"{label} (x, y)"] = tuple(keypoint)

        for angle_key in angle_keys:
            angle_value = angle_info_dict.get(angle_key, None)
            if angle_value:
                angle_value = ''.join([char for char in angle_value if char.isdigit() or char == '.'])  # Keep only digits and the decimal point
            row_data[angle_key] = angle_value

        # Append the data to the DataFrame
        df = df.append(row_data, ignore_index=True)
```



| Employee ID | Frame | Box x | Box y | Box width | Box height | Width-to-height ratio |
| ----------- | ----- | ----- | ----- | --------- | ---------- | --------------------- |
| 1           | 1     | 803   | 539   | 150       | 322        | 0.46583852            |
| 2           | 1     | 1023  | 520   | 130       | 336        | 0.38690478            |

| right_shoulder&right_elbow  - RIGHT_ELBOW - right_elbow&right_wrist | right_shoulder&right_elbow -  RIGHT_SHOULDER - right_shoulder&left_shoulder | right_shoulder&right_elbow -  RIGHT_SHOULDER - right_shoulder&right_hip | left_shoulder&left_elbow - LEFT_ELBOW -  left_elbow&left_wrist | left_shoulder&left_elbow - LEFT_SHOULDER  - right_shoulder&left_shoulder | left_shoulder&left_elbow - LEFT_SHOULDER  - left_shoulder&left_hip |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 134.7                                                        | 150                                                          | 25.8                                                         | 152.7                                                        | 45.5                                                         | 40.9                                                         |
| 141.2                                                        | 77.7                                                         | 11.8                                                         | 154.4                                                        | 108.5                                                        | 20.1                                                         |

| right_hip&right_knee  - RIGHT_KNEE - right_knee&right_ankle | right_hip&right_knee - RIGHT_HIP -  right_hip&left_hip | right_hip&right_knee - RIGHT_HIP -  right_shoulder&right_hip | left_hip&left_knee - LEFT_KNEE -  left_knee&left_ankle | left_hip&left_knee - LEFT_HIP -  right_hip&left_hip | left_hip&left_knee - LEFT_HIP -  left_shoulder&left_hip | right_shoulder&left_shoulder -  RIGHT_SHOULDER - right_shoulder&right_hip | right_shoulder&left_shoulder -  LEFT_SHOULDER - left_shoulder&left_hip | right_hip&left_hip - RIGHT_HIP -  right_shoulder&right_hip | right_hip&left_hip - LEFT_HIP -  left_shoulder&left_hip |
| ----------------------------------------------------------- | ------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------ | --------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ---------------------------------------------------------- | ------------------------------------------------------- |
| 140.5                                                       | 103.6                                                  | 116.7                                                        | 140.8                                                  | 76.6                                                | 116.9                                                   | 175.9                                                        | 4.6                                                          | 13                                                         | 166.5                                                   |
| 155.1                                                       | 55                                                     | 143.4                                                        | 151.9                                                  | 128.6                                               | 137.6                                                   | 89.5                                                         | 88.4                                                         | 88.3                                                       | 93.8                                                    |

| Fatigue or Active |
| ----------------- |
| 1                 |
| 1                 |

## VI. Problems

### 1. Lack of depth information

The YOLO-Pose model is used to capture the coordinates of human body keypoints in two-dimensional images. However, due to its lack of depth information, it might not accurately represent poses in three-dimensional space. The perspective effect of the camera can make body parts farther from the camera appear smaller, leading to a difference between the measured angles in the image and the actual angles in three-dimensional space.



## VII. Code

### 1. Generate table data for two workers, including keypoints and joint angles (input: video)

```python
# Get the output data, save it as a table
import pandas as pd
import matplotlib.pyplot as plt
from pydantic import BaseModel
import numpy as np
from ultralytics import YOLO

model = YOLO('yolov8n-pose.pt')
footage = 'videos/top_nonfatigue_pose_straight.MOV'
# results = model(footage)
results = model.predict(footage, save=True, conf=0.5)

output_name = 'training_data/top_nonfatigue_pose_straight.csv'
fatigue_or_not = '0'

class GetKeypoint(BaseModel):
    NOSE:           int = 0
    LEFT_EYE:       int = 1
    RIGHT_EYE:      int = 2
    LEFT_EAR:       int = 3
    RIGHT_EAR:      int = 4
    LEFT_SHOULDER:  int = 5
    RIGHT_SHOULDER: int = 6
    LEFT_ELBOW:     int = 7
    RIGHT_ELBOW:    int = 8
    LEFT_WRIST:     int = 9
    RIGHT_WRIST:    int = 10
    LEFT_HIP:       int = 11
    RIGHT_HIP:      int = 12
    LEFT_KNEE:      int = 13
    RIGHT_KNEE:     int = 14
    LEFT_ANKLE:     int = 15
    RIGHT_ANKLE:    int = 16
        
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

body_keypoints_example = BodyKeypoints([[0,0]] * 17)
limbs = get_limbs_from_keypoints(body_keypoints_example)
def calculate_and_get_angles_as_dict(keypoints_coords, limbs):
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
        
        vector_A = np.array(limb_1[1]) - np.array(limb_1[0]) if np.array_equal(limb_1[1], common_point) else np.array(limb_1[0]) - np.array(limb_1[1])
        vector_B = np.array(limb_2[1]) - np.array(limb_2[0]) if np.array_equal(limb_2[1], common_point) else np.array(limb_2[0]) - np.array(limb_2[1])
        
        angle = calculate_angle(vector_A, vector_B)
        key = f"{limb_1_name} - {KEYPOINT_LABELS[np.where((result_keypoint == common_point).all(axis=1))[0][0]]} - {limb_2_name}"
        value = f"{angle:.1f}°"
        
        angle_information[key] = value
        
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

adjacent_limbs = []

selected_limbs = [
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

# Generating all possible combinations
for i in range(len(selected_limbs)):
    for j in range(i + 1, len(selected_limbs)):
        limb1 = limbs[selected_limbs[i]]
        limb2 = limbs[selected_limbs[j]]
        
        # Convert keypoints to tuples for comparison
        limb1_tuples = [tuple(point) for point in limb1]
        limb2_tuples = [tuple(point) for point in limb2]

        # Checking if any keypoint in the second limb matches with the keypoints in the first limb
        if any(kp in limb1_tuples for kp in limb2_tuples):
            adjacent_limbs.append((selected_limbs[i], selected_limbs[j]))

KEYPOINT_LABELS = [
    "NOSE", "LEFT_EYE", "RIGHT_EYE", "LEFT_EAR", "RIGHT_EAR", "LEFT_SHOULDER",
    "RIGHT_SHOULDER", "LEFT_ELBOW", "RIGHT_ELBOW", "LEFT_WRIST", "RIGHT_WRIST",
    "LEFT_HIP", "RIGHT_HIP", "LEFT_KNEE", "RIGHT_KNEE", "LEFT_ANKLE", "RIGHT_ANKLE"
]

# Create an empty DataFrame with the required columns
columns = ["Employee ID", "Frame"] + [f"{keypoint} (x, y)" for keypoint in KEYPOINT_LABELS]


angle_keys = [
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

def calculate_angle(A, B):
#     Calculate angle between two vectors A and B.
    dot_product = np.dot(A, B)
    norm_A = np.linalg.norm(A)
    norm_B = np.linalg.norm(B)
    return np.arccos(dot_product / (norm_A * norm_B)) * (180/np.pi)

columns = ["Employee ID", "Frame"] + [f"{label} (x, y)" for label in KEYPOINT_LABELS] + angle_keys + ["Fatigue or not"]
df = pd.DataFrame(columns=columns)

prev_person_coordinates = [None, None]  # Assuming at most two employees, initialize with None

for idx in range(len(results)):
    if idx < len(results):
        keypoints_data = results[idx].keypoints.xy.cpu().numpy()
    else:
        keypoints_data = []

    distances_and_indices = []

    for person_idx, result_keypoint in enumerate(keypoints_data):
        if len(result_keypoint) == 0:
            continue
        get_keypoint = GetKeypoint()
        nose_coordinate = tuple(result_keypoint[get_keypoint.NOSE])
        
        matched_person_idx, distance = find_closest_person_distance(prev_person_coordinates, nose_coordinate)
        distances_and_indices.append((distance, matched_person_idx, person_idx, result_keypoint))

    # Sort based on distances and select the top two
    sorted_matches = sorted(distances_and_indices, key=lambda x: x[0])[:2]
        
    for distance, matched_person_idx, person_idx, result_keypoint in sorted_matches:
        if matched_person_idx is not None:
            row_data["Employee ID"] = matched_person_idx + 1
            prev_person_coordinates[matched_person_idx] = tuple(result_keypoint[get_keypoint.NOSE])

        body_keypoints = BodyKeypoints(result_keypoint)
        limbs = get_limbs_from_keypoints(body_keypoints)
        angle_info_dict = calculate_and_get_angles_as_dict(result_keypoint, limbs)
#         print(angle_info_dict)

        # Create a dictionary for the row data
        row_data = {
            "Employee ID": person_idx + 1,  #"Employee ID" = person_idx + 1
            "Frame": idx + 1,
        }
        for label, keypoint in zip(KEYPOINT_LABELS, result_keypoint):
            row_data[f"{label} (x, y)"] = tuple(keypoint)

        for angle_key in angle_keys:
            angle_value = angle_info_dict.get(angle_key, None)
            if angle_value:
                angle_value = ''.join([char for char in angle_value if char.isdigit() or char == '.'])  # Keep only digits and the decimal point
            row_data[angle_key] = angle_value
        row_data['Fatigue or not'] = fatigue_or_not
        # Append the data to the DataFrame
        df = df.append(row_data, ignore_index=True)

# Print out the table representation
print(df)
# save DataFrame to a CSV file
df.to_csv(output_name, index=False)
```

### 2. Generate Pose image about two workers at a specific frame 

```python
# This function is used to generate information about two workers at the same time
def plot_keypoints_with_multiple_datasets(keypoints_datasets, limbs_template):
# By default, the DPI (dots per inch) in Matplotlib is set to 80. So, to get a figure of size 1920x1080, 
# we can set the width to 24 inches (1920/80) and the height to 13.5 inches (1080/80).
    plt.figure(figsize=(24, 13.5))
    POINT_LABEL_COLOR = 'green'
    LINE_LABEL_COLOR = 'purple'
    INDICATOR_LINE_COLOR = 'orange'
    ANGLE_INDICATOR_LINE_COLOR = 'blue'
    ANGLE_LABEL_COLOR = 'black'
    OFFSET_ANGLES = [0, 45, 90, 135, 180, 225, 270, 315]

    for keypoints_coords in keypoints_datasets:
        # Extract limbs based on current keypoints
        body_keypoints = BodyKeypoints(keypoints_coords)
        limbs = get_limbs_from_keypoints(body_keypoints)

        # Draw key points
        for idx, keypoint in enumerate(keypoints_coords):
            plt.scatter(*keypoint, s=50, color='blue')
            label_position = (keypoint[0] + 10, keypoint[1] + 15)
            plt.annotate(KEYPOINT_LABELS[idx], label_position, fontsize=8, ha='right', color=POINT_LABEL_COLOR)

        # Draw lines and add labels
        for limb_name, limb in limbs.items():
            x_values = [limb[0][0], limb[1][0]]
            y_values = [limb[0][1], limb[1][1]]
            plt.plot(x_values, y_values, 'r-')

            mid_x = sum(x_values) / 2
            mid_y = sum(y_values) / 2
            offset = 0.02
            indicator_end_x = mid_x + offset
            indicator_end_y = mid_y + offset
            plt.plot([mid_x, indicator_end_x], [mid_y, indicator_end_y], '--', color=INDICATOR_LINE_COLOR)
            plt.annotate(limb_name, (indicator_end_x, indicator_end_y), fontsize=8, ha='right', color=LINE_LABEL_COLOR)

        angle_offsets = {}

        # Calculate and annotate angles for adjacent limbs
        for limb_1_name, limb_2_name in adjacent_limbs:
            limb_1 = limbs[limb_1_name]
            limb_2 = limbs[limb_2_name]
            
            common_point = None
            for point in limb_1:
                if any(np.array_equal(point, p) for p in limb_2):
                    common_point = np.array(point)
                    break

            if common_point is None:
                continue

            # Get vector A and B
            vector_A = np.array(limb_1[1]) - np.array(limb_1[0]) if np.array_equal(limb_1[1], common_point) else np.array(limb_1[0]) - np.array(limb_1[1])
            vector_B = np.array(limb_2[1]) - np.array(limb_2[0]) if np.array_equal(limb_2[1], common_point) else np.array(limb_2[0]) - np.array(limb_2[1])

            angle = calculate_angle(vector_A, vector_B)

            # Determine the offset for multiple angles at the same point
            if common_point.tobytes() not in angle_offsets:
                angle_offsets[common_point.tobytes()] = 0
            else:
                angle_offsets[common_point.tobytes()] += 1

            offset_angle = OFFSET_ANGLES[angle_offsets[common_point.tobytes()] % len(OFFSET_ANGLES)]
            offset_dx = 50 * np.cos(np.radians(offset_angle))
            offset_dy = 50 * np.sin(np.radians(offset_angle))

            end_point = common_point + np.array([offset_dx, offset_dy])

            plt.plot([common_point[0], end_point[0]], [common_point[1], end_point[1]], linestyle='--', color=ANGLE_INDICATOR_LINE_COLOR)
            plt.annotate(f"{angle:.1f}°", end_point, fontsize=8, ha='center', va='center', color=ANGLE_LABEL_COLOR)

    plt.gca().invert_yaxis()
    plt.axis('equal')
    plt.show()

keypoints_data = results[0].keypoints.xy.cpu().numpy()
datasets_to_plot = [keypoints_data[i] for i in range(len(keypoints_data))]
plot_keypoints_with_multiple_datasets(datasets_to_plot, limbs)

# for idx in range(len(keypoints_data)):
#     print("NO.%d person detected: " %(idx+1))
#     result_keypoint = keypoints_data[idx]
#     print(result_keypoint)
#     body_keypoints = BodyKeypoints(result_keypoint)
#     limbs = get_limbs_from_keypoints(body_keypoints)
#     angle_info_dict = calculate_and_get_angles_as_dict(result_keypoint, limbs)
#     print(angle_info_dict)
```



## VII. Reference:

https://learnopencv.com/human-pose-estimation-using-keypoint-rcnn-in-pytorch/

https://alimustoofaa.medium.com/yolov8-pose-estimation-and-pose-keypoint-classification-using-neural-net-pytorch-98469b924525

https://github.com/ultralytics/ultralytics/issues/1915