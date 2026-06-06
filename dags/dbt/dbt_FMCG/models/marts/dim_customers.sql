with customers AS (
    SELECT * FROM {{ ref('stg_fmcg_customers') }}
),
locations AS (
    SELECT * FROM {{ ref('int_locations_joined') }}
)
SELECT
    c.CustomerID,
    c.FirstName,
    c.MiddleInitial,
    c.LastName,
    c.Address,
    l.CityName,
    l.CountryName,
    l.CountryCode,
    l.Zipcode
FROM customers c
LEFT JOIN locations l ON c.CityID = l.CityID