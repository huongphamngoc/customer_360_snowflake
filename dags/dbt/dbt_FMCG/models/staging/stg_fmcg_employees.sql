WITH source AS (
    SELECT * FROM {{ source('FMCG', 'Employees') }}
)
SELECT
    "EmployeeID" AS EmployeeID,
    INITCAP(TRIM("FirstName")) AS FirstName,
    TRIM("MiddleInitial") AS MiddleInitial,
    INITCAP(TRIM("LastName")) AS LastName,
    CASE 
        WHEN "BirthDate" > GETDATE() THEN NULL 
        ELSE "BirthDate" 
    END AS BirthDate,
    CASE 
        WHEN UPPER(TRIM("Gender")) = 'F' THEN 'Female'
        WHEN UPPER(TRIM("Gender")) = 'M' THEN 'Male'
        ELSE 'N/A' 
    END AS Gender,
    "CityID" AS CityID,
    "HireDate" AS HireDate
FROM source