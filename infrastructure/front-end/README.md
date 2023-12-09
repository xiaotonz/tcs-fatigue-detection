# Tsc-Fatigue-Detection

This project, "tsc-fatigue", is an Angular application utilizing Angular version 16.0.0. It is configured with a range of dependencies to support various features including animations, forms, routing, and third-party integrations like Bootstrap and Chart.js.

## Getting Started

To get started with this project, follow these steps:

1. **Clone the repository**

   ```bash
   git clone https://github.com/rpeter249/tcs-fatigue-detection.git

   cd tcs-fatigue-detection/front-end
   ```

2. **Install npm packages**

   Install the npm packages as described in `package.json`:

   ```bash
   npm install
   ```

3. **Running the application**

   Use the following command to start the application. This command compiles the TypeScript source code and launches the application on a local server:

   ```bash
   npm start
   ```

   The application will be available at `http://localhost:4200`. The server watches for any changes in the source files and automatically reloads the browser.

   To stop the server, use `Ctrl-C`.


# Application Structure

Below is the high-level structure of the application:

```
front-end/
├── src/
│   ├── app/
│   │   ├── history-detail/               # History Detail Module
│   │   │   ├── history-filter/           # - History Filter Component
│   │   │   ├── history-trend/            # - History Trend Component
│   │   │   ├── user-detail/              # - User Detail Component
│   │   │   └── [history-detail component files]
│   │   │
│   │   ├── main-page/                    # Main Page Module
│   │   │   ├── gauge-dashboard/          # - Fatigue Indicator Dashboard Component
│   │   │   ├── home/                     # - First Employee Component
│   │   │   ├── home2/                    # - Second Employee Component
│   │   │   ├── notification/             # - Pop-up Notification Component
│   │   │   ├── top-bar/                  # - Top Bar Component
│   │   │   └── [main component files]
│   │   │
│   │   ├── model/                        # Models
│   │   │   ├── empList.model.ts          # - List of Employees
│   │   │   ├── employee.model.ts         # - Single Employee
│   │   │   └── history.model.ts          # - Fatigue History
│   │   │
│   │   ├── service/                      # Services
│   │   │   ├── api.service.ts            # - All REST API interactions
│   │   │   ├── employee-data.service.ts  # - Manages employee ID for routing
│   │   │   └── fatiguedetection.service.ts # - WebSocket to send fatigue index
│   │   │
│   ├── assets/                           # Assets
│   ├── index.html                        # Main HTML file
│   ├── styles.css                        # Global Styles
│   └── main.ts                           # Entry Point
│
├── angular.json                          # Angular CLI Config
├── tsconfig.json                         # TypeScript Config
└── package.json                          # NPM Dependencies

```


## npm Scripts

Here are some useful commands defined in `package.json`:

- `npm start`: Compiles the application and starts a local server, both in "watch mode".
- `npm run build`: Compiles the application and generates output in `dist/` directory.
- `npm run watch`: Watches the source files and recompiles them automatically upon any changes.
- `npm test`: Runs unit tests on the application using the Angular testing framework.


## Code scaffolding

Run `ng generate component component-name` to generate a new component. You can also use `ng generate directive|pipe|service|class|guard|interface|enum|module`.

## Build

Run `ng build` to build the project. The build artifacts will be stored in the `dist/` directory.

## Running unit tests

Run `ng test` to execute the unit tests via [Karma](https://karma-runner.github.io).

## Running end-to-end tests

Run `ng e2e` to execute the end-to-end tests via a platform of your choice. To use this command, you need to first add a package that implements end-to-end testing capabilities.

## Further help

To get more help on the Angular CLI use `ng help` or go check out the [Angular CLI Overview and Command Reference](https://angular.io/cli) page.

## Dependencies

The project relies on various dependencies:

- Angular core and supporting modules (v16.0.0)
- Bootstrap for UI components (v5.2.3)
- Chart.js for data visualization (v4.4.0)
- ngx-bootstrap for additional Bootstrap components (v11.0.2)
- RxJS for reactive programming (v7.8.0)

## Development Dependencies

For development, the project includes:

- Angular CLI for project management (v16.0.2)
- Jasmine and Karma for unit testing
- TypeScript for static typing (v5.0.2)
