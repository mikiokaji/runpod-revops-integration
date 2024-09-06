'''
Handles all interactions with Snowflake, such as connecting to the database,
loading data into tables, and handling schema creation.
'''

import snowflake.connector
from config import (SNOWFLAKE_USER, SNOWFLAKE_PASSWORD, SNOWFLAKE_ACCOUNT,
                    SNOWFLAKE_WAREHOUSE, SNOWFLAKE_DATABASE, SNOWFLAKE_SCHEMA)


# Function to connect to Snowflake
def connect_to_snowflake():
    conn = snowflake.connector.connect(
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        account=SNOWFLAKE_ACCOUNT,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA
    )
    return conn


# Function to load contacts into staging table
def load_contacts_to_staging(contacts):
    conn = connect_to_snowflake()
    cursor = conn.cursor()
    try:
        # Create the staging table if it doesn't exist
        cursor.execute("""
            CREATE OR REPLACE TABLE staging_contacts (
                id STRING,
                email STRING,
                first_name STRING,
                last_name STRING
            );
        """)

        # Truncate the staging table before reloading data
        cursor.execute("TRUNCATE TABLE staging_contacts;")

        # Insert contacts data into the staging table
        insert_query = """
        INSERT INTO staging_contacts (id, email, first_name, last_name)
        VALUES (%s, %s, %s, %s)
        """
        for contact in contacts['results']:
            cursor.execute(insert_query, (
                contact['id'],
                contact['properties'].get('email', 'Unknown'),
                contact['properties'].get('firstname', 'Unknown'),
                contact['properties'].get('lastname', 'Unknown')
            ))
        conn.commit()
        print("Contacts loaded into staging table.")
    finally:
        cursor.close()
        conn.close()


# Function to load companies into staging table
def load_companies_to_staging(companies):
    conn = connect_to_snowflake()
    cursor = conn.cursor()
    try:
        # Create the staging table for companies if it doesn't exist
        cursor.execute("""
            CREATE OR REPLACE TABLE staging_companies (
                id STRING,
                name STRING,
                industry STRING
            );
        """)

        # Truncate the staging table before reloading data
        cursor.execute("TRUNCATE TABLE staging_companies;")

        # Insert companies data into the staging table
        insert_query = """
        INSERT INTO staging_companies (id, name, industry)
        VALUES (%s, %s, %s)
        """
        for company in companies['results']:
            cursor.execute(insert_query, (
                company['id'],
                company['properties'].get('name', 'Unknown'),
                company['properties'].get('industry', 'Unknown')
            ))
        conn.commit()
        print("Companies loaded into staging table.")
    finally:
        cursor.close()
        conn.close()


# Function to load deals into staging table
def load_deals_to_staging(deals):
    conn = connect_to_snowflake()
    cursor = conn.cursor()
    try:
        # Create the staging table for deals if it doesn't exist
        cursor.execute("""
            CREATE OR REPLACE TABLE staging_deals (
                id STRING,
                amount STRING,
                close_date STRING,
                company_id STRING  -- Add company_id to link deals with companies
            );
        """)

        # Truncate the staging table before reloading data
        cursor.execute("TRUNCATE TABLE staging_deals;")

        # Insert deals data into the staging table
        insert_query = """
        INSERT INTO staging_deals (id, amount, close_date, company_id)
        VALUES (%s, %s, %s, %s)
        """
        for deal in deals['results']:
            company_id = deal['associations']['companies']['results'][0]['id'] if 'associations' in deal and 'companies' in deal['associations'] else None
            cursor.execute(insert_query, (
                deal['id'],
                deal['properties'].get('amount', '0'),
                deal['properties'].get('closedate', 'Unknown'),
                company_id  # Insert the associated company_id
            ))
        conn.commit()
        print("Deals loaded into staging table.")
    finally:
        cursor.close()
        conn.close()