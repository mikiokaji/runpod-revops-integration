import requests
import logging
from .config import HUBSPOT_API_KEY, HUBSPOT_API_URL

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Helper function to make API requests
def make_request(endpoint, params={}):
    url = f"{HUBSPOT_API_URL}/{endpoint}"
    headers = {
        "Authorization": f"Bearer {HUBSPOT_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx, 5xx)
        logger.info(f"Successfully made request to {url}")
        logger.debug(f"Response: {response.json()}")
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        return None
    except Exception as err:
        logger.error(f"Other error occurred: {err}")
        return None

# Fetch contacts from HubSpot
def get_contacts():
    endpoint = "crm/v3/objects/contacts"
    params = {"limit": 100}  # Limit the number of results per request
    return make_request(endpoint, params)

# Fetch companies from HubSpot
def get_companies():
    endpoint = "crm/v3/objects/companies"
    params = {"limit": 100}
    return make_request(endpoint, params)

# Fetch deals from HubSpot
def get_deals():
    endpoint = "crm/v3/objects/deals"
    params = {
        "limit": 100,  # Limit the number of results per request
        "associations": "companies"  # Include company associations in the response
    }
    return make_request(endpoint, params)

# Main function to test fetching data
if __name__ == "__main__":
    contacts = get_contacts()
    logger.info(f"Contacts: {contacts}")

    companies = get_companies()
    logger.info(f"Companies: {companies}")

    deals = get_deals()
    logger.info(f"Deals: {deals}")