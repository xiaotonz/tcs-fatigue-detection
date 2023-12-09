# TCS Fatigue Detection Model Deployment Overview

## Introduction

This project demonstrates a machine learning pipeline for video-based fatigue detection. The key steps are:

1. **Body Pose Estimation** - A pre-trained YOLOv8 model fine-tuned for body pose estimation is used to extract 17 body joint keypoints from video frames depicting workers. This gives (x,y) coordinates for joints like shoulders, elbows, wrists etc.

2. **Feature Engineering** - The frame-wise body keypoints are used to calculate inter-joint angles which serve as posture features. Velocity features are computed from displacement of joints over time.

3. **Model Training** - Two types of machine learning models are trained for fatigue classification:

   **XGBoost Model**

   - An XGBoost model is trained on both the body posture angles as well as velocity features.
   - It is configured as a binary classifier to categorize each video frame as either fatigue or non-fatigue.
   - Hyperparameter tuning is done to maximize the accuracy of this classifier.

   **Random Forest Model**

   - Two separate Random Forest models are trained targeting different goals:
     1. **Classification Model** - Trained to classify fatigue similar to the XGBoost model. Provides a class label output.
     2. **Regression Model** - Trained to predict the probability percentage of fatigue, essentially regressing the target to a continuous output variable. Provides a fatigue index between 0-100%.
   - So in summary, the XGBoost model and Random Forest classifier allow making discretepredictions of whether a frame shows fatigue or not. The Random Forest regressor predicts the likelihood or degree of fatigue.

4. **Deployment** - The trained models are packaged into a Docker container along with a FastAPI server for real-time fatigue classification. It processes a video stream, extracts features, loads models and returns per-person fatigue status via JSON.

5. **Integration** - The server can optionally save fatigue alerts to a database. It also pushes live notifications via websockets to alert monitoring dashboards.

So in summary, body joint keypoints and derived features are used to train ML models for classifying fatigue. The models are deployed in a containerized server which can interface with databases and external monitoring systems via standard integration APIs.



## Key Concepts in Model Deployment

- **Docker**: Used to containerize the model server for easy deployment and portability.

  Docker packages the model server code, libraries, and saved models into an image that can be instantiated as containers. This allows the server to be portable across environments.

- **Kubernetes (K8s)**: Orchestrates and manages containers running the model server at scale. 

  Kubernetes dynamically schedules and manages containers running the model server to optimize resource usage. Features like auto-scaling and self-healing provide resilience.

- **Terraform**: Provisions the cloud infrastructure needed to host the model server. 

  Terraform is used to provision and configure the virtual machines, storage, and networking resources needed to host the Docker containers orchestrated by Kubernetes.

- **Fastapi**: Provides a REST API server to accept video feeds and return fatigue detection results. 

  FastAPI provides the REST API endpoints to accept video feeds as input and return the fatigue detection results as JSON. It serves predictions by loading the saved ML models.



## Project Structure

```
model_deployment/
│
├── k8s/                                  # Kubernetes Configuration
│   ├── deployment.yaml                   # - Deployment Configuration
│   └── service.yaml                      # - Service Configuration
│
├── saved_models/                         # Machine Learning Models
│   ├── body_joint_random_forest_model.joblib  # - Body Joint Random Forest Model
│   ├── phase_segmentation_random_forest_model.joblib  # - Phase Segmentation Random Forest Model
│   ├── velocity_model_random_forest_model.joblib  # - Velocity Random Forest Model
│   ├── xgboost_model.pkl                 # - Body Joint XGBoost Model
│   └── yolov8n-pose.pt                   # - Keypoints detection YOLOv8 Pose Model
│
├── terraform/                            # Terraform Infrastructure
│   ├── main.tf                           # - Main Terraform Configuration
│   └── terraform.tfstate                 # - Terraform State File
│
├── training_models/                      # Model Training Scripts
│   ├── fatigue_detection_csv_data/       # - CSV Data for Training
│   │   ├── frontal_fatigue_pose_straight.csv  # - Frontal Fatigue Pose Data
│   │   ├── processed_nonfatigue_data.csv # - Processed Non-Fatigue Data
│   │   └── ...                           # - Other CSV Data Files
│   ├── phase_segmentation_csv_data/      # - CSV Data for Training
│   │   ├── frontal_fatigue_pose_straight_phase.csv  # - Frontal Fatigue Pose Data Labeled with Phase Data
│   │   ├── frontal_nonfatigue_pose_straight_phase.csv  # - Processed Non-Fatigue Data Labeled with Phase Data
│   │   └── ...                           # - Other CSV Data Files
│   ├── training_body_joint_model.py      # - Training Script for Body Joint Random Forest Model
│   ├── training_phase_segmentation_model.py  # - Training Script for Phase Segmentation Random Forest Model
│   └── training_velocity_model.py        # - Training Script for Velocity Random Forest Model
│
├── videos/                               # Video Files for Processing
│   ├── input_videos/                     # - Input Videos
│   │   ├── frontal_fatigue_pose_straight.MOV  # - Frontal Straight Angel Fatigue Pose Video
│   │   └── ...                           # - Other Input Videos
│   └── output_videos/                    # - Processed Output Videos
│       └── annotated_frontal_fatigue_pose_straight.mp4  # - Annotated Video
│
├── developer/                            # Development Scripts
│   ├── config.py                         # - Configuration Script
│   ├── constants.py                      # - Constants Definitions
│   ├── database.py                       # - Database Interaction Script
│   ├── models.py                         # - Model Definitions and Utilities
│   ├── utils.py                          # - Utility Functions
│   ├── video_processing_locally.py       # - Local Video Processing Script
│   ├── video_processing.py               # - Video Processing Script for Web
│   └── websocket_message.py              # - WebSocket Messaging Script
│
└── documents/                            # Documentation and Configurations
    ├── config.ini                        # - Configuration File
    ├── Dockerfile                        # - Docker Configuration
    └── requirements.txt                  # - Python Dependencies
```



#### Folders:

- **k8s Folder**: 
  - `deployment.yaml`: Defines Kubernetes deployment to run model server containers.
  - `service.yaml`: Sets up load balancer to distribute traffic to model server containers.
- **saved_models Folder**: 
  - `body_joint_random_forest_model.joblib`
    - Input Features: Body joint angles calculated from pose keypoints in each video frame. Captures posture of the person.
    - Training Data: Preprocessed body joint angle data extracted from sample input videos. Stored as CSV files in `csv_data` folder.
    - Model Architecture: Random forest classifier with 100 trees. Built using scikit-learn RandomForestClassifier.
    - Output: Predicts if a frame shows fatigue (1) or not (0). Also provides probability scores for fatigue/not fatigue classes.
    - Use: Loaded at runtime by model server to classify fatigue from body poses in new videos.
  - `velocity_model_random_forest_model.joblib`
    - Input Features: Velocity features including speed, acceleration etc calculated from body joint movements across video frames.
    - Training Data: Preprocessed velocity features data stored in CSV files under `csv_data` folder.
    - Model Architecture: Random forest model tuned via grid search cross-validation for optimal hyperparameters.
    - Output: Same as body joint model - predicts per frame fatigue status and probabilities.
    - Use: Alternative model to `body_joint_random_forest_model.joblib` for classifying fatigue based on body motions.
  - `xgboost_model.pkl`
    - Configured as a binary classifier to categorize each video frame as either fatigue or non-fatigue.
  - `yolov8n-pose.pt`: Pre-trained YOLOv8 body pose estimator to extract keypoints
- **terraform Folder**: 
  - `main.tf`: Provisions Azure VM and networking resources to host Kubernetes cluster.
  - `terraform.tfstate`: Tracks status of infrastructure provisioned by Terraform config.
- **training_models Folder**: 
  - **csv_data Folder**: Contains preprocessed CSV files used to train models.
    - frontal_fatigue_pose_straight.csv
    - processed_nonfatigue_data.csv
    - ......

  - `training_body_joint_model.py`: Trains random forest classifier on body joint angles data. Saves model to `body_joint_random_forest_model.joblib`.
  - `training_velocity_model.py`: Trains random forest classifier model on velocity features data using grid search. Saves best model to `velocity_model_random_forest_model.joblib`.
- **videos Folder**:
  - **input_videos Folder**: 
    - frontal_fatigue_pose_straight.MOV
    - ......

  - **output_videos Folder**: 
    - annotated_frontal_fatigue_pose_straight.mp4


#### Developer:

- `config.py`
  - Contains a single function, `read_config`, used for reading configuration settings.
  - **Function**: `read_config(config_file)`
    - **Input**: A string `config_file` which is the path to the configuration file.
    - **Output**: A `config` object containing the parsed configuration settings.
    - **Purpose**: To read and parse a configuration file (such as an .ini file) using `configparser` module. This is useful for separating configuration settings (like database credentials) from code.

- `constants.py`
  - Defines various constants used throughout the project.
    - `NNPACK_MODE`: Represents a configuration setting for a neural network package.
    - `VIDEO_CHUNK_SIZE`: Specifies the size of chunks (in bytes) when processing or downloading video data, used to manage memory and network bandwidth effectively.
    - `FRAME_PROCESS_INTERVAL`: Indicates the interval at which video frames are processed. For example, a value of 5 could mean that every fifth frame in a video is processed.
    - `UNKNOWN_EMPLOYEE`: A default string value representing an unknown employee, possibly used as a placeholder in cases where employee information is missing or not recognized.
    - `UNKNOWN_SHIFT`: Represents a default value for an unknown work shift, similar in purpose to `UNKNOWN_EMPLOYEE`.
    - `DATE_FORMAT`: Defines the format for date and time strings, ensuring consistency in how dates and times are recorded and displayed throughout the application.
    - `EMPLOYEE_ID`, `FRAME`, `BOX_X`, `BOX_Y`, `BOX_WIDTH`, `BOX_HEIGHT`, `WIDTH_TO_HEIGHT_RATIO`, `FATIGUE_STATUS`: These constants represent column names or data labels used in data processing or storage.
    - `DEFAULT_TIME`: A default timestamp, used as a fallback value in scenarios where an actual timestamp is not available.
    - `KEYPOINT_LABELS`: An array of strings, each representing a label for a keypoint in pose estimation (e.g., body parts like "NOSE", "LEFT_EYE").
    - `ANGLE_KEYS`: An array of strings that appear to define specific angles of interest between keypoints.
    - `SELECTED_LIMBS`: An array defining pairs of keypoints that form limbs.
    - `DATAFRAME_PREDICT_COLUMNS`: Specifies column names for a DataFrame, used in machine learning predictions. It combines basic employee and frame data with the `ANGLE_KEYS`.
    - `PREDICT_RECORD_COLUMNS`: Defines column names for prediction records, used when storing or displaying prediction results.

- `database.py`
  - Contains functions related to database operations.
  - **Function**: `initialize_database(config)`
    - **Input**: `config`, a configuration object.
    - **Output**: A tuple `(db_connection, db_cursor)` representing the database connection and cursor.
    - **Purpose**: To establish a connection with a database using credentials from a configuration object.
  - **Function**: `insert_or_update_employee(db_cursor, emp_id, emp_name, emp_position, emp_shift)`
    - **Input**: Database cursor `db_cursor`, and employee details `emp_id`, `emp_name`, `emp_position`, `emp_shift`.
    - **Purpose**: To insert a new employee record into the database or update it if it already exists.
  - **Function**: `insert_or_update_fatigue_history_index(db_connection, db_cursor, timestamp, emp_id, fatigue_index)`
    - **Input**: Database connection `db_connection`, cursor `db_cursor`, and fatigue-related data `timestamp`, `emp_id`, `fatigue_index`.
    - **Purpose**: To manage the insertion or updating of fatigue history records in the database.
  - **Function**: `insert_or_update_fatigue_history(db_connection, db_cursor, timestamp, emp_id)`
    - **Input**: Similar to `insert_or_update_fatigue_history_index`, but only `timestamp` and `emp_id` are used.
    - **Purpose**: To insert or update fatigue history records, focusing on employee identification and timestamp.

- `models.py`
  - Used for defining models and utility functions related to model loading and data handling.
  - **Function**: `load_model(model_file_path)`
    - **Input**: A string `model_file_path` representing the path to the model file.
    - **Output**: `loaded_model`, the machine learning model loaded from the file.
    - **Purpose**: To load a machine learning model from a given file path.
  - **Class**: `GetKeypoint`
    - **Purpose**: Defines an enumeration for body keypoints, used in pose estimation tasks.
  - **Class**: `BodyKeypoints`
    - **Purpose**: Represents a set of body keypoints. The constructor takes `keypoints` and assigns them to named attributes for easy access.
  - **Function**: `get_limbs_from_keypoints(keypoints: BodyKeypoints)`
    - **Input**: An instance of `BodyKeypoints`.
    - **Output**: A dictionary `limbs` mapping limb names to their corresponding keypoints.
    - **Purpose**: To derive limb information from body keypoints, useful in pose estimation and analysis.


- `utils.py`
  - Contains utility functions for video processing, angle calculations, and other general purposes.
  - **Function**: `download_video(video_url, video_file)`
    - **Input**: `video_url` (URL of the video to download) and `video_file` (path to save the downloaded video).
    - **Output**: An instance of `cv2.VideoCapture` if the download is successful; otherwise, `None`.
    - **Purpose**: To download a video from a given URL and prepare it for processing with OpenCV.
  - **Function**: `calculate_and_get_angles_as_dict(adjacent_limbs, result_keypoint, limbs)`
    - **Input**: A list of limb pairs `adjacent_limbs`, keypoints `result_keypoint`, and a dictionary `limbs`.
    - **Output**: A dictionary `angle_information` containing calculated angles.
    - **Purpose**: To calculate angles between adjacent limbs based on keypoints, used in pose analysis.
  - **Function**: `find_closest_person_distance(prev_coordinates, current_coordinate)`
    - **Input**: A list of previous coordinates `prev_coordinates` and a current coordinate `current_coordinate`.
    - **Output**: A tuple `(index, distance)` indicating the closest previous coordinate and its distance.
    - **Purpose**: To find the closest person's coordinates from a previous frame, useful in tracking movement over time.
  - **Function**: `calculate_angle(A, B)`
    - **Input**: Two vectors `A` and `B`.
    - **Output**: The calculated angle between the vectors.
    - **Purpose**: To calculate the angle between two vectors, used in pose analysis.


- `video_processing_locally.py`

  - The code implements local processing of video files to detect and analyze workers' fatigue. It integrates various modules for video processing, model prediction and database manipulation.
  - **Function**: `process_video_locally(input_video_file_path, output_video_name="None", load_local_video=False)`
    - Input:
      - `input_video_file_path`: Path to the input video file.
      - `output_video_name`: Name of the output video file, default is "None".
      - `load_local_video`: Boolean flag to indicate whether to load a local video or download from a URL.
    - **Output**: Processed video with fatigue analysis results, along with database updates.
    - **Purpose**: To process a video file locally by detecting workers, analyzing their postures using a machine learning model, predicting fatigue levels, and updating these results in a database. It also annotates the video with bounding boxes and status text.

- `video_processing.py`

  - This code is designed for processing videos in a web-based environment, using FastAPI for handling HTTP requests and WebSocket for real-time data communication.
  - **Function**: `process_video_endpoint(request: Request)`
    - **Input**: `request` object from FastAPI containing the video URL.
    - **Output**: JSON response indicating the processing status of the video.
    - **Purpose**: To initiate video processing from a provided URL through an HTTP GET request.
  - **Function**: `get_status(task_id: str)`
    - **Input**: `task_id`, a string representing the unique identifier of a processing task.
    - **Output**: JSON response with the status of the specified task.
    - **Purpose**: To provide the processing status of a video associated with a given task ID.
  - **Function**: `process_video(input_video_file_path, task_id)`
    - Input:
      - `input_video_file_path`: Path to the video file to be processed.
      - `task_id`: Unique identifier of the task.
    - **Output**: Processed video and updated task status.
    - **Purpose**: To process the video file for fatigue analysis, similar to `process_video_locally` but tailored for web-based requests.
  - **Function**: `websocket_endpoint(websocket: WebSocket)`
    - **Input**: `websocket`, a WebSocket connection.
    - **Output**: Engages in WebSocket communication.
    - **Purpose**: To handle real-time WebSocket communication, sending and receiving messages related to video processing tasks.
  - **Function**: `send_messages(websocket: WebSocket)`
    - **Input**: `websocket`, a WebSocket connection.
    - **Output**: Sends real-time updates over WebSocket.
    - **Purpose**: To continuously send messages over WebSocket to a client, updating them about the video processing status.

- `websocket_message.py`

  - Sets up a WebSocket server for real-time communication with clients.
  - **Function**: `handler(websocket, _)`
    - **Input**: `websocket`, a WebSocket connection; `_`, a placeholder for additional parameters.
    - **Output**: Maintains a continuous WebSocket connection, handling incoming messages.
    - **Purpose**: To handle incoming WebSocket messages from connected clients and maintain a list of active connections.
  - **Function**: `send_message(message)`
    - **Input**: `message`, a string to be sent to all connected WebSocket clients.
    - **Output**: Confirmation that the message was sent.
    - **Purpose**: To broadcast a message to all connected WebSocket clients.
  - **Function**: `start_server()`
    - **Input**: None.
    - **Output**: Running WebSocket server.
    - **Purpose**: To start and run the WebSocket server indefinitely, handling incoming connections and messages.


#### Documents:

* `config.ini`

  * Configuration file, used to set up various parameters and settings for the application.
  * **[model]**: Defines paths to various machine learning models and a parameter for processing intervals.
    - `yolo_model`: YOLO model path used for pose detection.
    - `xgboost_model`: XGBoost model path.
    - `body_joint_rf_model`: Random Forest model file path for body joint analysis.
    - `velocity_rf_model`: Random Forest model file path for velocity analysis.
    - `interval_frame`: An integer value indicating the frame interval.
  * **[db]**: Database configuration settings.
    - `host`: The database server's host address.
    - `user`: Database username.
    - `password`: Password for the database.
    - `database`: The name of the database to connect to.
  * **[data]**: Configuration related to data handling.
    - `video_file`: Path to the input video file.
    - `output_video`: Path where the processed video will be saved.
    - `video_url`: The default URL of the video to be processed.
    - `default_label`: A default label value.

* `Dockerfile`

  * Used to build a Docker container for the application.

* `requirements.txt`

  * Lists all the Python packages required for the application.

     


## Running Fatigue Detection Model locally

#### 1. Installing the required packages via requirement.txt

```bash
pip install -r requirements.txt
```

#### 2. Running video_processing_locally.py

```bash
python video_processing_locally.py videos/input_videos/frontal_fatigue_pose_straight.MOV
```



## Deploying a Fatigue Detection Model Service

### Step-by-Step Guide

#### 1. Build Docker image

```bash
docker build -t fatigue-detection-server .
```

#### 2. Push image to container registry

```bash
az acr create -n <acr-name> -g <resource-group> --sku Basic
az acr login -n <acr-name> 
docker tag fatigue-server <acr-name>.azurecr.io/fatigue-server
docker push <acr-name>.azurecr.io/fatigue-server
```

#### 3. Use Terraform to provision Azure VM for hosting Kubernetes cluster

```bash
cd terraform
terraform init
terraform apply
```

#### 4. SSH into VM to install Kubernetes

```bash
ssh azureuser@<public-ip>

# Install docker, kubeadm
sudo apt update
sudo apt install -y docker.io
curl https://aks.ms/install.sh | bash  

# Initialize Kubernetes cluster
sudo kubeadm init --pod-network-cidr=192.168.0.0/16

# Setup kubeconfig
mkdir ~/.kube
sudo cp /etc/kubernetes/admin.conf ~/.kube/config
sudo chown $(id -u):$(id -g) ~/.kube/config

# Install Flannel CNI   
kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
```

#### 5. Deploy model server pods

```bash
kubectl apply -f k8s
```

#### 6. Expose deployment via load balancer service

```bash
kubectl apply -f service.yaml
```

#### 7. Get load balancer IP

```bash
kubectl get service
```

To test, send sample video files to `<lb-ip>/process?url=http://<video-url>`



## Available Endpoints

#### 1. Get Video Processing Status

- **Endpoint**: `/status/{task_id}`
- **Method**: GET
- **Description**: Retrieves the current status of a video processing task. The endpoint requires a `task_id` as a path parameter to identify the specific task. It returns the status of the task and the original video URL.

#### 2. Process Video

- **Endpoint**: `/process`
- **Method**: GET
- **Description**: Initiates the processing of a video. This endpoint accepts a video URL as a query parameter. It assigns a unique `task_id` to the processing task and queues it for processing. Returns a confirmation message with the `task_id`.

#### 3. Get All Tasks

- **Endpoint**: `/tasks`
- **Method**: GET
- **Description**: Lists all video processing tasks with their current status. It provides an overview of all tasks that have been queued or are currently being processed, along with their respective `task_id` and video URLs.

#### 4. WebSocket Endpoint

- **Endpoint**: `/ws`
- **Method**: WebSocket
- **Description**: Establishes a WebSocket connection for real-time communication. This endpoint is used for sending real-time updates about video processing tasks to connected clients.
