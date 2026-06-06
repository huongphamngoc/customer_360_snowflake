WITH source AS (
    SELECT * FROM {{ source('FMCG', 'Categories') }}
)
SELECT
    "CategoryID" AS CategoryID,
    INITCAP(TRIM("CategoryName")) AS CategoryName
FROM source