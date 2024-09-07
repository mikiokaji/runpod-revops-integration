import logging
from .hubspot_api import get_contacts, get_companies, get_deals

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_contacts_from_hubspot():
    try:
        logger.info("Fetching contacts from HubSpot...")
        contacts = get_contacts()
        if contacts:
            logger.info("Contacts fetched successfully.")
        else:
            logger.warning("No contacts returned.")
        return contacts
    except Exception as e:
        logger.error(f"Error fetching contacts: {e}", exc_info=True)
        raise

def fetch_companies_from_hubspot():
    try:
        logger.info("Fetching companies from HubSpot...")
        companies = get_companies()
        if companies:
            logger.info("Companies fetched successfully.")
        else:
            logger.warning("No companies returned.")
        return companies
    except Exception as e:
        logger.error(f"Error fetching companies: {e}", exc_info=True)
        raise

def fetch_deals_from_hubspot():
    try:
        logger.info("Fetching deals from HubSpot...")
        deals = get_deals()
        if deals:
            logger.info("Deals fetched successfully.")
        else:
            logger.warning("No deals returned.")
        return deals
    except Exception as e:
        logger.error(f"Error fetching deals: {e}", exc_info=True)
        raise