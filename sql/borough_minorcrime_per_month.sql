SELECT 
    borough, 
    year, 
    month, 
    major_category, 
    minor_category, 
    SUM(value) AS no_crimes
FROM `bigquery-public-data.london_crime.crime_by_lsoa`
GROUP BY 
    minor_category, 
    major_category, 
    month, 
    year, 
    borough
ORDER BY 
    borough, 
    year, 
    month, 
    major_category, 
    minor_category
