-- Create a view for Deals associated with HubSpot companies
CREATE OR REPLACE VIEW company_deals AS
SELECT
    d.id AS deal_id,               -- Deal ID
    d.amount,                      -- Deal amount
    d.close_date,                  -- Deal close date
    c.id AS company_id,            -- HubSpot company ID
    c.name AS company_name         -- HubSpot company name
FROM
    staging_deals d                -- Staging table for deals
JOIN
    staging_companies c ON c.id = d.company_id -- Join with companies on company_id
WHERE
    d.amount IS NOT NULL;           -- Filter out deals without amounts