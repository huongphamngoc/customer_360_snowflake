WITH city AS (
    SELECT * FROM {{ ref('stg_fmcg_cities') }}
),
country AS (
    SELECT * FROM {{ ref('stg_fmcg_countries') }}
)
SELECT
    c.CityID,
    c.CityName,
    co.CountryID,
    co.CountryName,
    co.CountryCode,
    c.Zipcode
FROM city c
JOIN country co ON c.CountryID = co.CountryID