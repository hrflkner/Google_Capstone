SELECT
  borough,
  major_category,
  rank_per_borough,
  no_of_incidents
FROM (
  SELECT
    borough,
    major_category,
    RANK() OVER(PARTITION BY borough ORDER BY SUM(value) DESC) AS rank_per_borough,
    SUM(value) AS no_of_incidents
  FROM
    `bigquery-public-data.london_crime.crime_by_lsoa`
  GROUP BY
    borough,
    major_category )
WHERE
  borough = "Westminster"
ORDER BY
  borough,
  rank_per_borough
