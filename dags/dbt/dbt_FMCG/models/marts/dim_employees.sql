WITH employees AS (
    SELECT * FROM {{ ref('stg_fmcg_employees') }}
),
locations AS (
    SELECT * FROM {{ ref('int_locations_joined') }}
)
SELECT
    e.EmployeeID,
    e.FirstName,
    e.MiddleInitial,
    e.LastName,
    e.BirthDate,
    e.Gender,
    e.HireDate,
    l.CityName,
    l.CountryName,
    l.CountryCode,
    l.Zipcode
FROM employees AS e
LEFT JOIN locations AS l ON e.CityID = l.CityID