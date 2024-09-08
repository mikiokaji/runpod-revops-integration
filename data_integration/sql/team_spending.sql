CREATE OR REPLACE VIEW INTERVIEW_DATA_4.PUBLIC.team_spending AS
SELECT
    co.id AS company_id,
    co.name AS company_name,
    t.id AS team_id,
    t.name AS team_name
FROM
    INTERVIEW_DATA_4.PUBLIC.staging_companies co
JOIN
    INTERVIEW_DATA_4.PUBLIC.TEAM t 
ON 
    SOUNDEX(co.name) = SOUNDEX(t.name) -- Primary matching criteria
    OR t.name LIKE CONCAT('%', co.name, '%') -- Fallback match on partial names
GROUP BY
    co.id, co.name, t.id, t.name;