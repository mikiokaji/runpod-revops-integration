import logging
from dagster import op, job, In
from data_integration.snowflake_loader import (
    load_contacts_to_staging,
    load_companies_to_staging,
    load_deals_to_staging,
    execute_sql_script
)
from data_integration.hubspot_loader import (
    fetch_contacts_from_hubspot,
    fetch_companies_from_hubspot,
    fetch_deals_from_hubspot
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@op
def extract_contacts():
    try:
        contacts = fetch_contacts_from_hubspot()
        logger.info("Successfully extracted contacts from HubSpot.")
        return contacts
    except Exception as e:
        logger.error(f"Error extracting contacts from HubSpot: {e}")
        raise


@op
def extract_companies():
    try:
        companies = fetch_companies_from_hubspot()
        logger.info("Successfully extracted companies from HubSpot.")
        return companies
    except Exception as e:
        logger.error(f"Error extracting companies from HubSpot: {e}")
        raise


@op
def extract_deals():
    try:
        deals = fetch_deals_from_hubspot()
        logger.info("Successfully extracted deals from HubSpot.")
        return deals
    except Exception as e:
        logger.error(f"Error extracting deals from HubSpot: {e}")
        raise


@op(ins={"contacts": In()})
def load_contacts_to_snowflake_op(contacts):
    try:
        load_contacts_to_staging(contacts)
        logger.info("Successfully loaded contacts into Snowflake.")
    except Exception as e:
        logger.error(f"Error loading contacts into Snowflake: {e}")
        raise


@op(ins={"companies": In()})
def load_companies_to_snowflake_op(companies):
    try:
        load_companies_to_staging(companies)
        logger.info("Successfully loaded companies into Snowflake.")
    except Exception as e:
        logger.error(f"Error loading companies into Snowflake: {e}")
        raise


@op(ins={"deals": In()})
def load_deals_to_snowflake_op(deals):
    try:
        load_deals_to_staging(deals)
        logger.info("Successfully loaded deals into Snowflake.")
    except Exception as e:
        logger.error(f"Error loading deals into Snowflake: {e}")
        raise


@op
def execute_contacts_sql():
    try:
        execute_sql_script("data_integration/sql/contacts_to_users.sql")
        logger.info("Successfully executed contacts SQL script.")
    except Exception as e:
        logger.error(f"Error executing contacts SQL script: {e}")
        raise


@op
def execute_teams_sql():
    try:
        execute_sql_script("data_integration/sql/team_spending.sql")
        logger.info("Successfully executed teams SQL script.")
    except Exception as e:
        logger.error(f"Error executing teams SQL script: {e}")
        raise


@op
def execute_deals_sql():
    try:
        execute_sql_script("data_integration/sql/company_deals.sql")
        logger.info("Successfully executed deals SQL script.")
    except Exception as e:
        logger.error(f"Error executing deals SQL script: {e}")
        raise


@job(name="revops_pipeline_job")
def runpod_revops_pipeline():
    try:
        contacts = extract_contacts()
        companies = extract_companies()
        deals = extract_deals()

        load_contacts_to_snowflake_op(contacts)
        load_companies_to_snowflake_op(companies)
        load_deals_to_snowflake_op(deals)

        execute_contacts_sql()
        execute_teams_sql()
        execute_deals_sql()

        logger.info("Pipeline execution completed successfully.")
    except Exception as e:
        logger.error(f"Pipeline execution failed: {e}")
        raise