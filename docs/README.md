## Running the Dagster UI and Starting the Schedule

### 1. Setup and Prerequisites

Before proceeding, make sure you have the following setup:
- Python environment with Dagster and necessary dependencies installed.
- The `.env` file configured with your environment variables (e.g., `HUBSPOT_API_KEY`, `SNOWFLAKE_USER`, etc.).

### 2. Launching the Dagster Web UI

To start the Dagster web server and associated services, follow these steps:

1. Open a terminal and navigate to the project root directory.
2. Run the following command to launch Dagster:

   ```bash
   dagster dev -w dagster_pipeline/workspace.yaml

This command will start the Dagster web server, accessible at http://127.0.0.1:3000.

3. Open a browser and go to the web address shown in the logs.

### 3. Starting the every_minute_schedule
You can start the every_minute_schedule using either the Dagster UI or the command line. Here’s how to do it from the command line:

1. Open a new terminal window and run the following command to start the schedule:

    ```bash
    dagster schedule start -w dagster_pipeline/workspace.yaml --location repository.py every_minute_schedule

2. To verify that the schedule has started, use the following command:
   
    ```bash
    dagster schedule list -w dagster_pipeline/workspace.yaml --location repository.py

### 4. Viewing Pipeline Runs
Once the schedule is running, the pipeline will execute every minute. You can view the results of each run by navigating to the "Runs" section in the Dagster Web UI at http://127.0.0.1:3000.

Here, you will see logs and execution details for each pipeline run.

### 5. Stopping the Schedule

If you need to stop the every_minute_schedule, run the following command:

    dagster schedule stop -w dagster_pipeline/workspace.yaml --location repository.py every_minute_schedule

This will stop the schedule from running further.
