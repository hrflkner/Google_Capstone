SELECT
  borough,
  year,
  major_category,
  rank_per_borough,
  no_of_incidents
FROM (
  SELECT
    borough,
    year,
    major_category,
    RANK() OVER(PARTITION BY borough, year ORDER BY SUM(value) DESC) AS rank_per_borough,
    SUM(value) AS no_of_incidents
  FROM
    `bigquery-public-data.london_crime.crime_by_lsoa`
  GROUP BY
    borough,
    year,
    major_category )
WHERE
  borough = "Westminster"
ORDER BY
  borough,
  year,
  rank_per_borough
