# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 22:09:11 2021

@author: Hunter Faulkner
"""
#%% Imports

import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt

#%% Import Datasets

# Data from BigQuery Results
minor_permonth = pd.read_csv("filepath")
total_permonth = pd.read_csv("filepath")
total_peryear = pd.read_csv("filepath")
westminster_crimes = pd.read_csv("filepath")
westminster_crimes_by_year = pd.read_csv("filepath")
# Shapefile for Map
londonmap = gpd.read_file("filepath")

#%% Concat Year and Date Columns for plotting

minor_permonth["date"]=(minor_permonth[['year','month']
                            ].astype(str).agg('-'.join, axis=1)
                                ).astype('datetime64[ns]')

total_permonth["date"]=(total_permonth[['year','month']
                            ].astype(str).agg('-'.join, axis=1)
                                ).astype('datetime64[ns]')

total_peryear["date"]=(total_peryear[['year']
                            ].astype(str).agg('-'.join, axis=1)
                                ).astype('datetime64[ns]')

#%% Total per Month Long form to Wide form

# Borough List without City of London for the plotting loops
boroughs = set(total_permonth['borough'])-set(['City of London'])

total_permonth_wide = pd.DataFrame()
total_permonth_wide['date'] = set(total_permonth['date'])
for x in boroughs:
    total_permonth_wide[f'{x}'] = list(total_permonth[
        total_permonth['borough'] == f'{x}']['no_crimes'])


# Calculate Percent Change over each Month per Borough
perc_change = pd.DataFrame()
for x in boroughs:
    if x != 'City of London': # Remove City of London Outlier
        perc_change[f'{x}'] = ((total_permonth_wide[f'{x}'] -
                          total_permonth_wide[f'{x}'].shift(1)) /
                          total_permonth_wide[f'{x}']).fillna(0)
    else:
        pass

# Plot Cumulative Sum of Percent Change
plt.figure(figsize=(24,16))

plt.plot(total_permonth_wide['date'], 
             perc_change[f'{x}'].cumsum(), label=f'{x}')
plt.plot(total_permonth_wide['date'],total_permonth_wide['Merton'])
plt.plot(total_permonth_wide['date'],total_permonth_wide['Hillingdon'])
plt.legend()

plt.show()

#%% Join Map DataFrame with Crimes per year by Borough DataFrame

merge_mapcrimes = londonmap.set_index('NAME').join(
            total_peryear[total_peryear['year']==2016].set_index('borough')
            )

#%% Create Heatmap of London Crimes

fig, ax = plt.subplots(1, figsize=(32, 28))

plt.title("Total Crime in London Boroughs\n2016",
         size=40)
merge_mapcrimes.plot(column='no_crimes',
                     cmap="Reds",
                     ax=ax, 
                     linewidth=1,
                     edgecolor='0')
ax.axis('off')

plt.show()

#%% Westminster Analysis and Line Plot

westminstercrimes=minor_permonth[(minor_permonth['borough']=='Westminster') &
                    (minor_permonth['major_category']=='Theft and Handling')
                    ].groupby(['date','major_category'])['no_crimes'].sum()

plt.figure(figsize=(24,16))
plt.title("Violent Crimes in Westminster", fontsize=20)
plt.plot(np.unique(minor_permonth['date']),
         westminstercrimes)
plt.xlabel("Date", fontsize=16)
plt.ylabel("Number of Crimes", fontsize=16)

plt.show()

#%% Westminster Pie Chart

# Calculate Vector of Percentages
westminster_crimes['perc_total']=(westminster_crimes['no_of_incidents'] /
                               sum(westminster_crimes['no_of_incidents']))*100

# Plot Pie Chart of Percentages
fig,ax=plt.subplots(figsize=(24,16))
explodeby = (0.05,0.05,0.05,0.05,0.05,0.05,0.05)
ax.pie(westminster_crimes['perc_total'][0:7],
        labels=westminster_crimes['major_category'][0:7],
        explode=explodeby,
        autopct='%1.2f%%',
        textprops=dict(size=30))
plt.title("Westminster Major Crimes\nas a Percentage of Total Crime",
          fontsize=30)
ax.legend(loc="upper right",
          bbox_to_anchor=(1.4,1),
           fontsize=16)

plt.show()

#%%

crimesum = westminster_crimes_by_year.groupby('year')['no_of_incidents'].sum()

yearvars = pd.Series(list(set(westminster_crimes_by_year['year'])))
thefts = westminster_crimes_by_year[westminster_crimes_by_year[
                        'major_category']=='Theft and Handling'
                        ]['no_of_incidents']
violence = westminster_crimes_by_year[westminster_crimes_by_year[
                        'major_category']=='Violence Against the Person'
                        ]['no_of_incidents']
perc_thefts = pd.Series((thefts.values / crimesum.values) * 100)
perc_violence = pd.Series((violence.values / crimesum.values) * 100)

plt.figure(figsize=(20, 10))
labels = sorted(list(yearvars))
inc = np.arange(9)
width = .2
ax = plt.subplot(111)
ax.set_xticks(inc)
ax.set_xticklabels(labels, fontsize=16)
plt.title('Westminster Thefts and Violence\nas a Percentage of Total Crimes',
          fontsize=20)
plt.xlabel('Date', 
           fontsize=16)
plt.ylabel('Percentage', 
           fontsize=16)
ax.bar(inc - width, perc_thefts,
       label = 'Theft and Handling',
       width = .35, color='navy')
ax.bar(inc + width, perc_violence,
       label = 'Violence Against the Person',
       width = .35, color='firebrick')
plt.axhline(0, alpha=.5)
plt.legend(fontsize=16)
plt.grid(alpha=0.3)
plt.show()