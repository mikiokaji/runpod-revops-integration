-- Create a view that links HubSpot companies with Snowflake teams and calculates total team spending
CREATE OR REPLACE VIEW team_spending AS
SELECT
    co.id AS company_id,              -- HubSpot company ID
    co.name AS company_name,          -- HubSpot company name
    t.team_id,                        -- Team ID from the TEAM table
    t.team_name,                      -- Team name from the TEAM table
    SUM(tr.amount) AS totalTeamSpend  -- Sum of all transactions to calculate total team spending
FROM
    staging_companies co              -- Staging table containing HubSpot companies
JOIN
    TEAM_MEMBERSHIP tm ON co.id = tm.company_id -- Join HubSpot company with TEAM_MEMBERSHIP
JOIN
    TEAM t ON tm.team_id = t.team_id  -- Join TEAM_MEMBERSHIP with the TEAM table
LEFT JOIN
    TRANSACTION tr ON tm.user_id = tr.user_id  -- Join with transactions to calculate total spending for the team
GROUP BY
    co.id, co.name, t.team_id, t.team_name;  -- Group by company and team details for aggregation
