'''
Handles the extraction of data from HubSpot's API. This will include
fetching the raw data, formatting it, and preparing it for insertion.
'''

import logging
from snowflake_loader import load_contacts_to_staging, load_companies_to_staging, load_deals_to_staging
from hubspot_api import get_contacts, get_companies, get_deals

# Configure logging
logging.basicConfig(level=logging.INFO)

def fetch_contacts_from_hubspot():
    try:
        logging.info("Fetching contacts from HubSpot...")
        contacts = get_contacts()
        logging.info("Contacts fetched successfully.")
        return contacts
    except Exception as e:
        logging.error(f"Error fetching contacts: {e}", exc_info=True)
        raise

def fetch_companies_from_hubspot():
    try:
        logging.info("Fetching companies from HubSpot...")
        companies = get_companies()
        logging.info("Companies fetched successfully.")
        return companies
    except Exception as e:
        logging.error(f"Error fetching companies: {e}", exc_info=True)
        raise

def fetch_deals_from_hubspot():
    try:
        logging.info("Fetching deals from HubSpot...")
        deals = get_deals()
        logging.info("Deals fetched successfully.")
        return deals
    except Exception as e:
        logging.error(f"Error fetching deals: {e}", exc_info=True)
        raise