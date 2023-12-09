# tcs-fatigue-detection
Capstone Fall 23 , TCS fatigue detection project

This README outlines the architecture and setup required to deploy the Fatigue Detection Project. The project aims to deliver a comprehensive solution for identifying signs of fatigue using machine learning models based on computer vision. Additionally, it includes a frontend interface developed with Angular to display alerts, notifications, and employee shift information. The backend infrastructure is hosted on Azure and encompasses hosting the machine learning model, implementing APIs, and managing the database.

## Project Deliverables:
- Machine Learning Model: Utilizing computer vision techniques to detect signs of fatigue from video input.
- Frontend Interface: Developed with Angular to showcase alerts, notifications, and employee shift details.
- Backend Cloud Service: Hosted on Azure, encompassing the machine learning model, APIs, and database for seamless functionality.

The following sections provide guidance on setting up and deploying the architecture for this fatigue detection project.

## Project Setup

### Setting up Project Components

You can set up the project components in two ways:

#### 1. Using Terraform Scripts

Navigate to the location `infrastructure/terraform/main.tf` and execute the following commands:

```
terraform init
terraform plan
terraform apply
```

Ensure to add the subscription ID, database username, and password before running these commands. This process will automatically create the SQL database and Kubernetes cluster as specified in the Terraform scripts.

### Manual Setup on Azure Platform

**a. Azure Database Setup:**

1. Access Azure Database for MySQL Flexible Server.
2. Create a Flexible Server:
   - Choose the subscription, a name, location, and resource group (or create a new one).
   - Select your preferred MySQL version, compute, and storage configurations.
   - Opt for MySQL authentication and set the username and password.
   - Review your configurations and create the server.

**b. Kubernetes Services Setup:**

1. Access Kubernetes Services on Azure.
2. Create a new Kubernetes service:
   - Choose the subscription, resource group (or create a new one), and define the service name.
   - Configure the service according to the preferred production standard and select the desired region.
  
**c. Azure Container registry Setup:**

1. Access Container registries
2. Create a container registry:
   - Choose the sucscription, a name, location, and resource group (or create a new one).
   - Select pricing plan

This manual process enables the step-by-step creation of Azure Database for MySQL Flexible Server Kubernetes services, and container registry, allowing you to customize settings and configurations as needed.

## Code Deployment

### Database and Table Creation

- Head to `databases/create_table.sql` and execute the provided SQL commands on the database.
- Insert initial user data as needed. You can use `databases/insert_queries.sql`.

### Service Setup

1. **Azure Authentication:**
   - Log in to Azure via the command line using `az login`. Additionally, authenticate into the container registry using `az acr login -n tcsFatigueAcr` (replace with the repository name).

2. **Backend Setup:**

   - Access the backend folder and run:
     ```
     docker build -t tcsfatigueacr.azurecr.io/tcs-web-app .
     ```
     (Replace `tcs-web-app` with the backend image name)
   
   - Push the image to the container registry:
     ```
     docker push tcsfatigueacr.azurecr.io/tcs-web-app
     ```
   
   - Navigate to `back-end/k8s` and apply the configurations:
     ```
     kubectl apply -f .
     ```
   
   - Check deployment status using:
     ```
     kubectl get deployments
     kubectl get services
     ```
     Note the IP address for `tcs-web-app-service` for frontend connectivity.

3. **Models Deployment:**

   - Follow similar steps for models deployment as with the Backend Setup.
   - Note the IP address for `tcs-model-service` for WebSocket connections in the frontend.

4. **Front-end Deployment:**

   - Navigate to the front-end folder and make required changes in files.
   - Build the image:
     ```
     docker build -t tcsfatigueacr.azurecr.io/tcs_front_end .
     ```
     (Replace `tcs_front_end` with the frontend image name)
   
   - Push the image to the container registry:
     ```
     docker push tcsfatigueacr.azurecr.io/tcs_front_end
     ```
   
   - Apply the configurations in `back-end/k8s`:
     ```
     kubectl apply -f .
     ```
   
   - Verify deployment status using:
     ```
     kubectl get deployments
     kubectl get services
     ```

### Setup Testing

- Access various services using respective IP addresses.
- For testing purposes:
  - Access `http://20.237.111.52/` (replace with the tcs-model IP address) to establish WebSocket connections.
  - Trigger a job using the command:
    ```
    http://20.237.111.52/process?url=https://tcsfatiguemlen1658192275.blob.core.windows.net/asset-505652fb-70d9-4bf1-8df7-bc33f6a5f000/test_video%20(1).mp4
    ```
    (replace `20.237.111.52` with the tcs-model IP address)
  - Visit the front-end URL via the `angular-app-service` to ensure proper frontend functionality.


     

  


   

