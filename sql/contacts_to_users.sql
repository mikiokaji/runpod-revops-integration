-- Create a view that links HubSpot contacts with Snowflake users and calculates clientLifeTimeSpend
CREATE OR REPLACE VIEW contacts_to_users AS
SELECT
    c.id AS contact_id,               -- HubSpot contact ID
    c.first_name,                     -- HubSpot contact first name
    c.last_name,                      -- HubSpot contact last name
    u.user_id,                        -- Snowflake user ID from the USER table
    u.email,                          -- Email from the USER table
    SUM(t.amount) AS clientLifeTimeSpend -- Sum of transactions to calculate total spend by this user
FROM
    staging_contacts c                -- Staging table containing HubSpot contacts
JOIN
    USER u ON c.email = u.email       -- Join on email between HubSpot contacts and Snowflake users
LEFT JOIN
    TRANSACTION t ON u.user_id = t.user_id -- Join with transactions to calculate total spending
GROUP BY
    c.id, c.first_name, c.last_name, u.user_id, u.email;  -- Group by contact and user details for aggregation