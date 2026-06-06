WITH source AS (
    SELECT * FROM {{ source('FMCG', 'Customers') }}
)
SELECT  
    "CustomerID" AS CustomerID,
    INITCAP(TRIM("FirstName")) AS FirstName,
    TRIM("MiddleInitial") AS MiddleInitial,
    INITCAP(TRIM("LastName")) AS LastName,
    "CityID" AS CityID,
    TRIM("Address") AS Address
FROM source