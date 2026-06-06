WITH source AS (
    SELECT * FROM {{ source('FMCG', 'Countries') }}
)
SELECT 
    "CountryID" AS CountryID,
    INITCAP(TRIM("CountryName")) AS CountryName,
    TRIM("CountryCode") AS CountryCode
FROM source