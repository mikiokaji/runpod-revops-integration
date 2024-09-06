import requests
from .config import HUBSPOT_API_KEY, HUBSPOT_API_URL

# Helper function to make API requests
def make_request(endpoint, params={}):
    url = f"{HUBSPOT_API_URL}/{endpoint}"
    headers = {
        "Authorization": f"Bearer {HUBSPOT_API_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        print(response.json())  # Log the full API response to inspect the fields
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
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
    # Test each function
    contacts = get_contacts()
    print("Contacts:", contacts)

    companies = get_companies()
    print("Companies:", companies)

    deals = get_deals()
    print("Deals:", deals)