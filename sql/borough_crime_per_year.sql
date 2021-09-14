SELECT borough, year, SUM(value) AS no_crimes
FROM `bigquery-public-data.london_crime.crime_by_lsoa`
GROUP BY year, borough
ORDER BY borough, year
