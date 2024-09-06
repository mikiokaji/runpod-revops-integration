from dotenv import load_dotenv
import os

# Load the environment variables from the .env file
load_dotenv()

# HubSpot API configuration
HUBSPOT_API_KEY = os.getenv("HUBSPOT_API_KEY")
HUBSPOT_API_URL = "https://api.hubapi.com"

# Raise an error if the API key is not set
if HUBSPOT_API_KEY is None:
    raise ValueError("HubSpot API key is not set in the .env file")

# Snowflake connection configuration
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA")

# Raise an error if any Snowflake credentials are not set
if not all([SNOWFLAKE_USER, SNOWFLAKE_PASSWORD, SNOWFLAKE_ACCOUNT, SNOWFLAKE_WAREHOUSE, SNOWFLAKE_DATABASE, SNOWFLAKE_SCHEMA]):
    raise ValueError("One or more Snowflake credentials are not set in the .env file")