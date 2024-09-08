CREATE OR REPLACE VIEW INTERVIEW_DATA_4.PUBLIC.company_deals AS
SELECT
    d.id AS deal_id,               -- Deal ID
    d.amount,                      -- Deal amount
    d.close_date,                  -- Deal close date
    c.id AS company_id,            -- HubSpot company ID (from companies table)
    COALESCE(c.name, d.company_name) AS company_name -- Use staging_companies' name or the name from staging_deals
FROM
    INTERVIEW_DATA_4.PUBLIC.staging_deals d
LEFT JOIN
    INTERVIEW_DATA_4.PUBLIC.staging_companies c
    ON COALESCE(c.name, '') LIKE CONCAT('%', d.company_name, '%')  -- Match deals with companies
WHERE
    d.amount IS NOT NULL;           -- Filter out deals without amounts