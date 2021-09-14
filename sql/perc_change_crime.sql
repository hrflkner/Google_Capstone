SELECT
  borough,
  no_crimes_2008,
  no_crimes_2016,
  no_crimes_2016 - no_crimes_2008 AS change,
  ROUND(((no_crimes_2016 - no_crimes_2008) / no_crimes_2016) * 100, 2) AS perc_change
FROM (
  SELECT
    borough,
    SUM(IF(year=2008, value, NULL)) no_crimes_2008,
    SUM(IF(year=2016, value, NULL)) no_crimes_2016
  FROM
    `bigquery-public-data.london_crime.crime_by_lsoa`
  GROUP BY
    borough )
ORDER BY
  perc_change ASC
