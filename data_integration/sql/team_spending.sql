CREATE OR REPLACE VIEW INTERVIEW_DATA_4.PUBLIC.team_spending AS
SELECT
    co.id AS company_id,
    co.name AS company_name,
    t.id AS team_id,
    t.name AS team_name,
    SUM(tr.amount) AS total_team_spend -- Aggregating total spending for the team
FROM
    INTERVIEW_DATA_4.PUBLIC.staging_companies co
JOIN
    INTERVIEW_DATA_4.PUBLIC.TEAM t
    ON SOUNDEX(co.name) = SOUNDEX(t.name) -- Primary matching criteria
    OR t.name LIKE CONCAT('%', co.name, '%') -- Fallback match on partial names
LEFT JOIN
    INTERVIEW_DATA_4.PUBLIC.TEAM_MEMBERSHIP tm
    ON t.id = tm.team_id -- Join with Team_Membership table
LEFT JOIN
    INTERVIEW_DATA_4.PUBLIC.TRANSACTION tr
    ON tm.member_user_id = tr.user_id -- Join with Transaction table to sum team spending
GROUP BY
    co.id, co.name, t.id, t.name;