from dotenv import load_dotenv
import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the environment variables from the .env file
load_dotenv()

# Add PYTHONPATH to sys.path
python_path = os.getenv('PYTHONPATH')
if python_path:
    sys.path.append(python_path)
    logger.info(f"PYTHONPATH set to: {python_path}")

# HubSpot Configuration
HUBSPOT_API_KEY = os.getenv("HUBSPOT_API_KEY")
HUBSPOT_API_URL = os.getenv("HUBSPOT_API_URL", "https://api.hubapi.com")

# Raise an error if the API key is not set
if HUBSPOT_API_KEY is None:
    logger.error("HubSpot API key is not set in the .env file")
    raise ValueError("HubSpot API key is not set in the .env file")

# Snowflake Configuration
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA")

# Raise an error if any Snowflake credentials are not set
if not all([SNOWFLAKE_USER, SNOWFLAKE_PASSWORD, SNOWFLAKE_ACCOUNT, SNOWFLAKE_WAREHOUSE, SNOWFLAKE_DATABASE, SNOWFLAKE_SCHEMA]):
    logger.error("One or more Snowflake credentials are not set in the .env file")
    raise ValueError("One or more Snowflake credentials are not set in the .env file")

logger.info("Environment variables loaded successfully.")
