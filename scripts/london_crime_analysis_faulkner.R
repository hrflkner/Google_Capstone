# Import Datasets
minor_permonth <- read.csv("minorcrime_perborough_permonth.csv")
total_permonth <- read.csv("total_crimes_perborough_permonth.csv")
total_peryear <- read.csv("total_crimes_perborough_peryear.csv")

total_permonth$date <- as.yearmon(paste(total_permonth$year,
                                        total_permonth$month),
                                  "%Y %m")

# Figure 1
ggplot(data = total_permonth, 
       aes(x = date, 
           y = no_crimes,
           group = borough)) + 
  geom_line(aes(color=borough)) +
  geom_text(x = 2015, 
            y = 4500, 
            label = "Westminster", 
            size = 8) +
  geom_text(x = 2015, 
            y = 250, 
            label = "City of London", 
            size = 8) +
  labs(
    title="Total Crimes per Borough per Month",
    subtitle="2008-2016",
    x = "Date",
    y = "Number of Reported Crimes",
    color = "Boroughs of London"
  ) +
  theme_minimal()