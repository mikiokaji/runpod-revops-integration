'''
Handles the extraction of data from HubSpot's API. This will include
fetching the raw data, formatting it, and preparing it for insertion.
'''
import logging
from snowflake_loader import load_contacts_to_staging, load_companies_to_staging, load_deals_to_staging
from hubspot_api import get_contacts, get_companies, get_deals

def main():
    try:
        logging.info("Starting the HubSpot data extraction process.")

        # Fetch data from HubSpot API
        logging.info("Fetching contacts...")
        contacts = get_contacts()
        logging.info("Contacts fetched successfully.")

        logging.info("Fetching companies...")
        companies = get_companies()
        logging.info("Companies fetched successfully.")

        logging.info("Fetching deals...")
        deals = get_deals()
        logging.info("Deals fetched successfully.")

        # Load data into Snowflake
        logging.info("Loading contacts into Snowflake...")
        load_contacts_to_staging(contacts)
        logging.info("Contacts loaded into Snowflake successfully.")

        logging.info("Loading companies into Snowflake...")
        load_companies_to_staging(companies)
        logging.info("Companies loaded into Snowflake successfully.")

        logging.info("Loading deals into Snowflake...")
        load_deals_to_staging(deals)
        logging.info("Deals loaded into Snowflake successfully.")

        logging.info("HubSpot data extraction and load process completed successfully.")

    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=True)

if __name__ == "__main__":
    main()