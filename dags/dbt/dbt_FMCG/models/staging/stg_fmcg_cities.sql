WITH source AS (
    SELECT * FROM {{ source('FMCG', 'Cities') }}
)
SELECT 
    "CityID" AS CityID,
    INITCAP(TRIM("CityName")) AS CityName,
    TRIM("Zipcode") AS Zipcode,
    "CountryID" AS CountryID
FROM source