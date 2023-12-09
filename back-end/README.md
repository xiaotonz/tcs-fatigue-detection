# TCS Employee Fatigue Backend

This Node.js application provides APIs for managing employee data and fatigue history.

## Installation

1. Run docker build and docker exec in the parent folder of backend to locally build and run the container

## Configuration

Update the `config.js` file with appropriate configurations for the database and server port.

## Project Structure

```
back-end/
├── k8s/
│   ├── service.yaml                    #  Kubernetes service configuration
│   ├── deployment.yaml                 # Kubernetes deployment configuration
├── Dockerfile                          # Instructions for building Docker images
├── README.md                           # Main project documentation file
├── config.js                           # Configuration file for application settings
├── index.js                            # Entry point file for the Node.js application
├── package-lock.json                   # Detailed dependency information for Node.js packages
├── package.json                        # Specification of Node.js dependencies and project details
```

- **k8s**
  - `service.yaml`: Kubernetes service configuration
  - `deployment.yaml`: Kubernetes deployment configuration
- `.dockerignore`: List of files/folders to ignore during Docker builds
- `Dockerfile`: Instructions for building Docker images
- `README.md`: Main project documentation file
- `config.js`: Configuration file for application settings
- `index.js`: Entry point file for the Node.js application
- `package-lock.json`: Detailed dependency information for Node.js packages
- `package.json`: Specification of Node.js dependencies and project details

## Available Endpoints

### Get Employees

- **Endpoint:** `/employee/list`
- **Method:** GET
- **Description:** Retrieves a list of all employees.

### Get Employee by ID

- **Endpoint:** `/employee/empId/:empId`
- **Method:** GET
- **Description:** Retrieves details of an employee based on their ID.

### Get Shifts

- **Endpoint:** `/shift/shiftId/:shiftId`
- **Method:** GET
- **Description:** Retrieves employees working in a specific shift based on the shift ID.

### Get Shift Numbers

- **Endpoint:** `/shift/shiftNumbers`
- **Method:** GET
- **Description:** Retrieves a list of distinct shift numbers.

### Get Fatigue History by Employee ID

- **Endpoint:** `/history/empId/:empId`
- **Method:** GET
- **Description:** Retrieves fatigue history for an employee based on their ID.

### Get Fatigue History by Duration

- **Endpoint:** `/history/duration/:duration`
- **Method:** GET
- **Description:** Retrieves fatigue history for a specified duration (week, fortnight, month).

## Database

This application connects to a MySQL database hosted at 'tcs-fatigue-server.mysql.database.azure.com'. Ensure the database and credentials are correctly configured. (Update these credentials as the password is insecure)

## Dependencies

- Express: Web application framework
- Axios: HTTP client for making requests
- Body-parser: Parsing middleware for handling JSON data
- MySQL: MySQL database driver


