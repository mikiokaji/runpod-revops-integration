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

@op
def extract_contacts():
    contacts = fetch_contacts_from_hubspot()
    return contacts

@op
def extract_companies():
    companies = fetch_companies_from_hubspot()
    return companies

@op
def extract_deals():
    deals = fetch_deals_from_hubspot()
    return deals

@op(ins={"contacts": In()})
def load_contacts_to_snowflake_op(contacts):
    load_contacts_to_staging(contacts)

@op(ins={"companies": In()})
def load_companies_to_snowflake_op(companies):
    load_companies_to_staging(companies)

@op(ins={"deals": In()})
def load_deals_to_snowflake_op(deals):
    load_deals_to_staging(deals)

@op
def execute_contacts_sql():
    execute_sql_script("data_integration/sql/contacts_to_users.sql")

@op
def execute_teams_sql():
    execute_sql_script("data_integration/sql/team_spending.sql")

@op
def execute_deals_sql():
    execute_sql_script("data_integration/sql/company_deals.sql")

@job
def runpod_revops_pipeline():
    contacts = extract_contacts()
    companies = extract_companies()
    deals = extract_deals()

    load_contacts_to_snowflake_op(contacts)
    load_companies_to_snowflake_op(companies)
    load_deals_to_snowflake_op(deals)

    execute_contacts_sql()
    execute_teams_sql()
    execute_deals_sql()