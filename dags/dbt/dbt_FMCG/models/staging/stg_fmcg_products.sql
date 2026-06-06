WITH source AS (
    SELECT * FROM {{ source('FMCG', 'Products') }}
)
SELECT
    "ProductID" AS ProductID,
    INITCAP(TRIM("ProductName")) AS ProductName,
    "Price" AS Price,
    "CategoryID" AS CategoryID,
    INITCAP(TRIM("Class")) AS Class,
    "ModifyDate" AS ModifyDate,
    INITCAP(TRIM("Resistant")) AS Resistant,
    INITCAP(TRIM("IsAllergic")) AS IsAllergic,
    "VitalityDays" AS VitalityDays
FROM source