-- Create a view for Deals associated with HubSpot companies
CREATE OR REPLACE VIEW INTERVIEW_DATA_4.PUBLIC.company_deals AS
SELECT
    d.id AS deal_id,               -- Deal ID
    d.amount,                      -- Deal amount
    d.close_date,                  -- Deal close date
    c.id AS company_id,            -- HubSpot company ID
    c.name AS company_name         -- HubSpot company name
FROM
    INTERVIEW_DATA_4.PUBLIC.staging_deals d  -- Fully qualified staging_deals table
JOIN
    INTERVIEW_DATA_4.PUBLIC.staging_companies c ON c.id = d.company_id  -- Fully qualified staging_companies table, ensuring correct join
WHERE
    d.amount IS NOT NULL            -- Filter out deals without amounts
    AND d.company_id IS NOT NULL;   -- Ensure deals have a valid company association