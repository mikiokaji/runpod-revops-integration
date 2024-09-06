-- Create a view that links HubSpot contacts with Snowflake users and calculates clientLifeTimeSpend
CREATE OR REPLACE VIEW INTERVIEW_DATA_4.PUBLIC.contacts_to_users AS
SELECT
    c.id AS contact_id,               -- HubSpot contact ID
    c.first_name,                     -- HubSpot contact first name
    c.last_name,                      -- HubSpot contact last name
    u.id AS user_id,                  -- Snowflake user ID from the USER table
    u.email,                          -- Email from the USER table
    SUM(t.amount) AS clientLifeTimeSpend -- Sum of transactions to calculate total spend by this user
FROM
    INTERVIEW_DATA_4.PUBLIC.staging_contacts c  -- Fully qualified HubSpot contacts table
JOIN
    INTERVIEW_DATA_4.PUBLIC.USER u ON c.email = u.email  -- Fully qualified USER table
LEFT JOIN
    INTERVIEW_DATA_4.PUBLIC.TRANSACTION t ON u.id = t.user_id  -- Fully qualified TRANSACTION table
GROUP BY
    c.id, c.first_name, c.last_name, u.id, u.email;  -- Group by contact and user details for aggregation