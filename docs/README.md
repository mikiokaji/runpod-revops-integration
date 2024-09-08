# RunPod RevOps Integration Project: HubSpot to Snowflake Pipeline

## Architecture Overview

The following architecture illustrates the flow of data from the HubSpot API to the final Snowflake views.

```text
                     HubSpot API  
                    (Contacts, Companies, Deals)
                             |
                             v
                  --------------------------------
                  |  Dagster Pipelines            |
                  |  (Fetch & Process Data)       |
                  --------------------------------
                             |
                             v
            ---------------------------------------------
            | Snowflake Staging Tables                  |
            | (staging_contacts, staging_companies,     |
            |  staging_deals)                           |
            ---------------------------------------------
                             |
                             v
       -----------------------------------------------
       | Snowflake Business Logic Database            |
       | (Users, Teams, Team Membership, Transactions)|
       -----------------------------------------------
                             |
                             v
        ----------------------------------------
        | Snowflake Final Views                 |
        | - contacts_to_users                   |
        | - team_spending                       |
        ----------------------------------------
```

### Flow Explanation

1. **HubSpot API**: The data source for fetching contacts, companies, and deals.
2. **Dagster Pipelines**: Executes data ingestion and transformation logic, pulling data from HubSpot and processing it for Snowflake.
3. **Snowflake Staging Tables**: Temporary tables where the raw data from HubSpot is stored for further processing.
4. **Snowflake Business Logic Database**: Stores user, team, and membership data, used to enrich HubSpot data.
5. **Snowflake Final Views**: The final output of the pipeline that aggregates the data into actionable insights, like `contacts_to_users` and `team_spending`.


## Setup and Running Instructions

### 1. Clone the Repository

First, clone the project repository to your local environment:

```bash
git clone https://github.com/your-repository/runpod-revops-integration.git
```

Navigate to the project directory:
```bash
cd runpod-revops-integration
```

### 2. Create and Activate a Virtual Environment

It is recommended to create a virtual environment to manage dependencies. Follow these steps:

- Create a virtual environment: `python -m venv venv`

- Activate the virtual environment:

On macOS/Linux: `source venv/bin/activate`

On Windows: `venv\Scripts\activate`

### 3. Install Dependencies

With the virtual environment activated, install the required dependencies: `pip install -r requirements.txt`

### 4. Configure Environment Variables

Create an `.env` file in the root directory of the project with the following structure (you’ll need to fill in the actual values):

```commandline
HUBSPOT_API_KEY=your_hubspot_api_key
HUBSPOT_API_URL=https://api.hubapi.com
SNOWFLAKE_USER=your_snowflake_user
SNOWFLAKE_PASSWORD=your_snowflake_password
SNOWFLAKE_ACCOUNT=your_snowflake_account
SNOWFLAKE_WAREHOUSE=your_snowflake_warehouse
SNOWFLAKE_DATABASE=your_snowflake_database
SNOWFLAKE_SCHEMA=your_snowflake_schema
PYTHONPATH=/path/to/your/local/runpod-revops-integration
```

#### 4.1 `pyproject.toml` Configuration

The project includes a pyproject.toml file in the dagster_pipeline folder with specific configuration settings for Dagster. Make sure to review and update this file if necessary, particularly the following section:

```toml
[tool.dagster]
home = "/Users/your-username/dagster_home"
```

- The `home` variable defines the path where Dagster stores its metadata and logs. Ensure this path exists on your machine, and modify it to your local environment if needed.

### 5. Launching the Dagster Web UI

This project uses Dagster for pipeline orchestration. To launch the Dagster web UI and services:

1. Open a terminal and navigate to the project root directory.

2. Start Dagster by running the following command: `dagster dev -w dagster_pipeline/workspace.yaml`

This command will start the Dagster web server, accessible at `http://127.0.0.1:3000`.

3. Open a browser and go to the provided web address to view the Dagster web UI.

### 6. Running the Data Pipeline

Once the Dagster web server is running, follow these steps to run the pipeline:

#### 6.1 Starting the `every_minute_schedule` (Optional)

The project has a pre-configured schedule, `every_minute_schedule`, that triggers the pipeline every minute. You can start this schedule using either the UI or the command line.

1. Open a new terminal window and run the following command to start the schedule:
`dagster schedule start -w dagster_pipeline/workspace.yaml --location repository.py every_minute_schedule`

2. To verify that the schedule has started, use this command:
`dagster schedule list -w dagster_pipeline/workspace.yaml --location repository.py`

#### 6.2 Viewing Pipeline Runs
Once the schedule is running, the pipeline will execute every minute. You can monitor the results by navigating to the "Runs" section in the Dagster Web UI at `http://127.0.0.1:3000`. There, you will find logs and detailed execution results for each run.

#### 6.3 Manually Triggering the Pipeline
If you want to trigger the pipeline manually, you can do so through the Dagster Web UI by navigating to the pipeline and clicking on “Launch Run.”

#### 7. Stopping the Schedule
To stop the `every_minute_schedule`, run this command:
`dagster schedule stop -w dagster_pipeline/workspace.yaml --location repository.py every_minute_schedule`

This will stop the schedule and prevent it from executing further.

## Data Model Explanation
The data model for this project integrates data from two primary sources: HubSpot CRM and the Business Logic Database (Snowflake). The goal is to combine this data to gain insights into contact spending and team-based spend.

### 1. HubSpot CRM Data
HubSpot's CRM system provides the following key entities via API:

- Contacts: Individuals associated with companies, identified by email and unique IDs.
- Companies: Businesses linked to contacts and deals.
- Deals: Sales transactions linked to companies and optionally associated with contacts.

#### Key HubSpot Relationships:

- A Company may have multiple Contacts.
- A Deal can involve multiple Companies.

#### HubSpot Data Fields:

- Contacts: `id`, `email`, `first_name`, `last_name`, `company_id`
- Companies: `id`, `name`, `industry`
- Deals: `id`, `amount`, `close_date`, `company_name`,  `company_id` (linked to companies)

### 2. Business Logic Database (Snowflake)

This database stores internal business data, specifically customer accounts, teams, transactions, and their memberships. These tables are used to link with HubSpot data, allowing us to calculate lifetime spend for users and total spend for teams.

#### Business Logic Database Tables:
- **Users**: RunPod users, linked to HubSpot contacts via email or `user_id`.
- **Teams**: Groups of users within RunPod, linked to HubSpot companies via partial name matching.
- **Team_Membership**: Relationship between users and teams.
- **Transactions**: Details of user transactions, used for calculating spending metrics.

#### Snowflake Data Fields:
- Users Table:
  - `user_id`: Unique identifier for each user. 
  - `user_name`: The name of the user. 
  - `email`: User’s email address, used for matching with HubSpot contacts.

- Teams Table:
  - `team_id`: Unique identifier for each team.
  - `team_name`: The name of the team, used to link with HubSpot companies.

- Team_Membership Table:
  - `user_id`: Identifier linking a user to a team.
  - `team_id`: Identifier linking the user to a specific team. 

- Transactions Table:
  - `user_id`: Identifier for the user making the transaction. 
  - `amount`: The value of the transaction.

#### Snowflake Data Fields:

The following views have been created to link the HubSpot data with the Snowflake data to achieve the project goals:

#### 1. `company_deals` View

This view joins deals with HubSpot companies to provide a list of deals associated with each company:

**Fields in this View:**
- `deal_id`: The ID of the deal.
- `amount`: The monetary value of the deal.
- `close_date`: The date the deal was closed.
- `company_id`: The ID of the associated HubSpot company.
- `company_name`: The name of the HubSpot company.

#### 2. `coontacts_to_users` View

This view links HubSpot contacts with Snowflake users and calculates each user’s total lifetime spend:

**Fields in this View:**
- `contact_id`: The ID of the HubSpot contact.
- `first_name`: The contact’s first name.
- `last_name`: The contact’s last name.
- `user_id`: The ID of the linked Snowflake user.
- `email`: The email of the linked user.
- `clientLifeTimeSpend`: The total lifetime spend of the user.

#### 3. `team_spending` View

This view links HubSpot companies to Snowflake teams and calculates the total spending for each team:

**Fields in this View:**
- `company_id`: The ID of the HubSpot company.
- `company_name`: The name of the HubSpot company.
- `team_id`: The ID of the Snowflake team.
- `team_name`: The name of the team.
- `totalTeamSpend`: The total amount spent by the team.

### 3. Data Pipeline
1. Extract: Data is fetched from HubSpot (Contacts, Companies, Deals) and loaded into Snowflake staging tables.
2. Transform: Contacts are linked to internal users, and deals are aggregated by team.
3. Load: Final views in Snowflake provide:
- Contact Spending: Total lifetime spending per contact.
- Team Spending: Total deal spend per team.

## Any Assumptions Made During Development

### 1. HubSpot API Rate Limits:
It is assumed that the rate limits for the HubSpot API will not be exceeded during normal operation. The pipeline does not currently implement retry logic for rate limit errors, but this could be added in future iterations if necessary.

### 2. HubSpot Data Completeness:
We assume that the data returned from HubSpot (such as contacts, companies, and deals) is accurate and complete. Missing or incomplete fields (e.g., emails, company names) are handled with fallback values (e.g., `'Unknown'`).

### 3. Data Consistency Between HubSpot and Snowflake:
We assume that the HubSpot data and Snowflake user accounts are aligned. Specifically, contacts fetched from HubSpot can be associated with user accounts in the Snowflake database based on available fields.

### 4. Snowflake Schema Availability:
The required Snowflake tables (`staging_contacts`, `staging_companies`, `staging_deals`) are assumed to exist or can be created dynamically by the pipeline. The schema provided during development is correct and aligned with business logic.

### 5. Team and User Association in Snowflake:
We assume that the relationship between HubSpot contacts and Snowflake user accounts (via teams) is correctly represented in the Snowflake tables (`Team`, `User`, and `Team_Membership` tables).

### 6. Environment Configuration:
We assume that the `.env` file is correctly configured with all required API keys, credentials, and URLs. Missing or incorrect values may lead to failures when interacting with HubSpot or Snowflake.

### 7. Snowflake Connection Stability:
It is assumed that the connection to Snowflake is stable during pipeline runs. Temporary connection issues are not accounted for in the current error-handling mechanisms but could be handled with retry logic if required.

### 8. Pipeline Scheduling:
Multiple pipeline schedules are defined to allow flexibility in execution frequency. While the `every_minute_schedule` was used for demonstration purposes, other schedules, such as `every_five_minutes_schedule` and `every_hour_schedule`, are also available for more realistic production scenarios. It is assumed that the chosen schedule will meet the operational needs without causing performance bottlenecks, API rate limit issues, or system overload.

- `every_minute_schedule`: Useful for rapid testing or scenarios requiring near real-time data ingestion.
- `every_five_minutes_schedule`: A more practical frequency for lightweight operations.
- `every_hour_schedule`: Suitable for less time-sensitive tasks, particularly when handling large data loads or reducing API calls.

It is assumed that these schedules can be adjusted based on production requirements and are flexible enough to handle varying data volumes without issues.