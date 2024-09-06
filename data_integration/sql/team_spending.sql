-- Create a view that links HubSpot companies with Snowflake teams and calculates total team spending
CREATE OR REPLACE VIEW INTERVIEW_DATA_4.PUBLIC.team_spending AS
SELECT
    co.id AS company_id,              -- HubSpot company ID
    co.name AS company_name,          -- HubSpot company name
    t.id AS team_id,                  -- Team ID from the TEAM table
    t.name AS team_name,              -- Team name from the TEAM table
    SUM(tr.amount) AS totalTeamSpend  -- Sum of all transactions to calculate total team spending
FROM
    INTERVIEW_DATA_4.PUBLIC.staging_companies co              -- Fully qualified staging_companies table
JOIN
    INTERVIEW_DATA_4.PUBLIC.TEAM t ON t.name LIKE CONCAT('%', co.name, '%')  -- Match partial company name with team name
LEFT JOIN
    INTERVIEW_DATA_4.PUBLIC.TEAM_MEMBERSHIP tm ON t.id = tm.team_id -- Join TEAM_MEMBERSHIP on team_id
LEFT JOIN
    INTERVIEW_DATA_4.PUBLIC.TRANSACTION tr ON tm.member_user_id = tr.user_id  -- Join with transactions to calculate total spending
GROUP BY
    co.id, co.name, t.id, t.name;  -- Group by company and team details for aggregation