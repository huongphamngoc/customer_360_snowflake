WITH products AS (
    SELECT * FROM {{ ref('stg_fmcg_products') }}
),
categories AS (
    SELECT * FROM {{ ref('stg_fmcg_categories') }}
)
SELECT
    p.ProductID,
    p.ProductName,
    c.CategoryID,
    c.CategoryName,
    p.Price,
    p.Class,
    p.ModifyDate,
    p.Resistant,
    p.IsAllergic,
    p.VitalityDays
FROM products p
LEFT JOIN categories c ON p.CategoryID = c.CategoryID