'''
Handles all interactions with Snowflake, such as connecting to the database,
loading data into tables, and handling schema creation.
'''

import logging
import snowflake.connector
from .config import (SNOWFLAKE_USER, SNOWFLAKE_PASSWORD, SNOWFLAKE_ACCOUNT,
                    SNOWFLAKE_WAREHOUSE, SNOWFLAKE_DATABASE, SNOWFLAKE_SCHEMA)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to connect to Snowflake
def connect_to_snowflake():
    try:
        conn = snowflake.connector.connect(
            user=SNOWFLAKE_USER,
            password=SNOWFLAKE_PASSWORD,
            account=SNOWFLAKE_ACCOUNT,
            warehouse=SNOWFLAKE_WAREHOUSE,
            database=SNOWFLAKE_DATABASE,
            schema=SNOWFLAKE_SCHEMA
        )
        logger.info("Successfully connected to Snowflake.")
        return conn
    except Exception as e:
        logger.error(f"Error connecting to Snowflake: {e}")
        raise

# Function to load contacts into staging table
def load_contacts_to_staging(contacts):
    conn = connect_to_snowflake()
    cursor = conn.cursor()
    try:
        logger.info("Creating staging_contacts table if not exists.")
        cursor.execute("""
            CREATE OR REPLACE TABLE staging_contacts (
                id STRING,
                email STRING,
                first_name STRING,
                last_name STRING
            );
        """)

        logger.info("Truncating staging_contacts table.")
        cursor.execute("TRUNCATE TABLE staging_contacts;")

        logger.info("Inserting contacts into staging_contacts.")
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
        logger.info("Contacts loaded into staging table successfully.")
    except Exception as e:
        logger.error(f"Error loading contacts into Snowflake: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

# Function to load companies into staging table
def load_companies_to_staging(companies):
    conn = connect_to_snowflake()
    cursor = conn.cursor()
    try:
        logger.info("Creating staging_companies table if not exists.")
        cursor.execute("""
            CREATE OR REPLACE TABLE staging_companies (
                id STRING,
                name STRING,
                industry STRING
            );
        """)

        logger.info("Truncating staging_companies table.")
        cursor.execute("TRUNCATE TABLE staging_companies;")

        logger.info("Inserting companies into staging_companies.")
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
        logger.info("Companies loaded into staging table successfully.")
    except Exception as e:
        logger.error(f"Error loading companies into Snowflake: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

# Function to load deals into staging table
def load_deals_to_staging(deals):
    conn = connect_to_snowflake()
    cursor = conn.cursor()
    try:
        logger.info("Creating staging_deals table if not exists.")
        cursor.execute("""
            CREATE OR REPLACE TABLE staging_deals (
                id STRING,
                amount STRING,
                close_date STRING,
                company_id STRING,
                company_name STRING  -- Add company_name for clarity
            );
        """)

        logger.info("Truncating staging_deals table.")
        cursor.execute("TRUNCATE TABLE staging_deals;")

        logger.info("Inserting deals into staging_deals.")
        insert_query = """
        INSERT INTO staging_deals (id, amount, close_date, company_id, company_name)
        VALUES (%s, %s, %s, %s, %s)
        """
        for deal in deals['results']:
            # Handle potential null values for amount and close_date
            amount = deal['properties'].get('amount', '0')
            close_date = deal['properties'].get('closedate', 'Unknown')

            # Extract the first company id from associations, if available
            company_id = None
            if 'associations' in deal and 'companies' in deal['associations']:
                company_results = deal['associations']['companies']['results']
                if company_results:
                    company_id = company_results[0]['id']

            # Extract the company name from dealname, assuming it's formatted as "CompanyName - DealName"
            dealname = deal['properties'].get('dealname', '')
            company_name = dealname.split(" - ")[0] if " - " in dealname else None

            # Insert the deal into Snowflake
            cursor.execute(insert_query, (
                deal['id'],
                amount,
                close_date,
                company_id,
                company_name
            ))

        conn.commit()
        logger.info("Deals loaded into staging table successfully.")
    except Exception as e:
        logger.error(f"Error loading deals into Snowflake: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

# Function to execute SQL scripts
def execute_sql_script(file_path):
    conn = connect_to_snowflake()
    cursor = conn.cursor()
    try:
        logger.info(f"Executing SQL script: {file_path}")
        with open(file_path, 'r') as sql_file:
            sql_script = sql_file.read()
            cursor.execute(sql_script)
            conn.commit()
            logger.info(f"Successfully executed {file_path}")
    except Exception as e:
        logger.error(f"Error executing SQL script {file_path}: {e}")
        raise
    finally:
        cursor.close()
        conn.close()