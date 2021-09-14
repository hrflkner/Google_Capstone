SELECT 
    borough,
    SUM(IF(year=2008, value, NULL)) AS no_crimes_2008,
    SUM(IF(year=2009, value, NULL)) AS no_crimes_2009,
    SUM(IF(year=2010, value, NULL)) AS no_crimes_2010,
    SUM(IF(year=2011, value, NULL)) AS no_crimes_2011,
    SUM(IF(year=2012, value, NULL)) AS no_crimes_2012,
    SUM(IF(year=2013, value, NULL)) AS no_crimes_2013,
    SUM(IF(year=2014, value, NULL)) AS no_crimes_2014,
    SUM(IF(year=2015, value, NULL)) AS no_crimes_2015,
    SUM(IF(year=2016, value, NULL)) AS no_crimes_2016
    #COUNT( major_category ) AS no_crimes
FROM `bigquery-public-data.london_crime.crime_by_lsoa`
GROUP BY 
    borough
ORDER BY 
    borough
