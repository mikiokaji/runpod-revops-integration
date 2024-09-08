CREATE OR REPLACE VIEW INTERVIEW_DATA_4.PUBLIC.contacts_to_users AS
SELECT
    c.id AS contact_id,               -- HubSpot contact ID
    c.first_name,                     -- HubSpot contact first name
    c.last_name,                      -- HubSpot contact last name
    u.id AS user_id,                  -- Snowflake user ID from the USER table
    u.email,                          -- Email from the USER table
    u.CLIENT_LIFETIME_SPEND           -- Use the pre-existing clientLifeTimeSpend from the USER table
FROM
    INTERVIEW_DATA_4.PUBLIC.staging_contacts c  -- HubSpot contacts
JOIN
    INTERVIEW_DATA_4.PUBLIC.USER u ON c.email = u.email;  -- Snowflake USER table