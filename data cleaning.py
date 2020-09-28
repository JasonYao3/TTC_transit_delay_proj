# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 12:20:11 2020

@author: Jason
"""

import pandas as pd
import numpy as np

bus_df = pd.read_csv('./data/merged_bus.csv', encoding='Latin-1')
streetcar_df = pd.read_csv('./data/merged_streetcar.csv', encoding='Latin-1')
subway_df = pd.read_csv('./data/merged_subway.csv', encoding='Latin-1')

# Bus data set

# Report Date column: Split year, month and day into 3 columns by "-"

bus_df['report_year'] = bus_df['Report Date'].apply(lambda x: int(x.split('-')[0]))
bus_df['report_month'] = bus_df['Report Date'].apply(lambda x: int(x.split('-')[1]))
bus_df['report_day'] = bus_df['Report Date'].apply(lambda x: int(x.split('-')[2]))

# Route
# According to TTC Routes in Numerical Order: All Time Listing
# https://transittoronto.ca/bus/8108.shtml
# There is no route number between 700 to 899
#print(bus_df.Route.unique())
bus_df = bus_df[~(bus_df['Route'] >= 700) & (bus_df['Route'] <900)]

# Time - break down by hour and min.
bus_df['time_hour'] = bus_df['Time'].apply(lambda x: int(x.split(':')[0]))
bus_df['time_min'] = bus_df['Time'].apply(lambda x: int(x.split(':')[1]))


# Missing Values
missing_vals_bus = bus_df.isnull().sum() / bus_df.shape[0]
missing_vals_bus[missing_vals_bus > 0].sort_values(ascending=False)

# Min Delay

# Min Delay: negative not sure what that means, 0 means 0 min delay and NaN means no record
# All Min Delay and Delay columns mean the same thing, they are just name different. They could be merged into one Min Delay column where the NaN rows and the non NaN rows combine together

bus_df['Min Delay'].fillna(bus_df[' Min Delay'], inplace=True)
bus_df['Min Delay'].fillna(bus_df['Delay'], inplace=True)

# Negative time 
bus_df['Min Delay'] = bus_df['Min Delay'].apply(lambda x: np.abs(x))

# Min Gap
# Bus
bus_df['Min Gap'].fillna(bus_df['Gap'], inplace=True)
# Negative time
bus_df['Min Gap'] = bus_df['Min Gap'].apply(lambda x: np.abs(x))

# Direction
# There are about 1000 different records of direction. From numbers to descriptions.
# Example of a description: No damage. No injuries Cleared at 17:24 by cab 107.                           1
print(bus_df.Direction.value_counts())

# Drop duplicate columns  Min Delay, Delay and Gap
bus_df.drop(columns=[' Min Delay', 'Delay','Gap'], inplace=True)

# Remove Min delay rows if NaN
bus_df = bus_df[bus_df['Min Delay'].notna()]

# From ImportData
# function to remove the leading and trailing white space in the data frame
def trim(dataset):
  # using .strip() to remove the leading and the trailing white spaces in each cell
  trim = lambda x: x.strip() if type(x) is str else x
  return dataset.applymap(trim)

bus_df = trim(bus_df)

# Rename columns
bus_df = bus_df.rename(columns = {'Report Date':'report_date', 'Min Delay': 'min_delay', 'Min Gap':'min_gap', 'Incident ID':'incident_id' })

# Street car
streetcar_df['report_year'] = streetcar_df['Report Date'].apply(lambda x: int(x.split('-')[0]))
streetcar_df['report_month'] = streetcar_df['Report Date'].apply(lambda x: int(x.split('-')[1]))
streetcar_df['report_day'] = streetcar_df['Report Date'].apply(lambda x: int(x.split('-')[2]))

# Subway
subway_df['report_year'] = subway_df['Date'].apply(lambda x: int(x.split('-')[0]))
subway_df['report_month'] = subway_df['Date'].apply(lambda x: int(x.split('-')[1]))
subway_df['report_day'] = subway_df['Date'].apply(lambda x: int(x.split('-')[2]))




# Street Car
streetcar_df['time_hour'] = streetcar_df['Time'].apply(lambda x: int(x.split(':')[0]))
streetcar_df['time_min'] = streetcar_df['Time'].apply(lambda x: int(x.split(':')[1]))

# Subway
subway_df['time_hour'] = subway_df['Time'].apply(lambda x: int(x.split(':')[0]))
subway_df['time_min'] = subway_df['Time'].apply(lambda x: int(x.split(':')[1]))

# Route:
# !00 Flemington Route -> Flemington Route



# Bus

# Street Car
missing_vals_streetcar = streetcar_df.isnull().sum() / streetcar_df.shape[0]
missing_vals_streetcar[missing_vals_streetcar > 0].sort_values(ascending=False)

streetcar_df['Min Delay'].fillna(streetcar_df['Delay'], inplace=True)

# Negative time 
streetcar_df['Min Delay'] = streetcar_df['Min Delay'].apply(lambda x: np.abs(x))


# Subway
missing_vals_subway = subway_df.isnull().sum() / subway_df.shape[0]
missing_vals_subway[missing_vals_subway > 0].sort_values(ascending=False)



# Street Car
streetcar_df['Min Gap'].fillna(streetcar_df['Gap'], inplace=True)


streetcar_df.drop(columns=['Delay','Gap'], inplace=True)


# Same thing goes to the Min Gap and Gap column. Merge them together into one column

# Incident ID only occurs on April 2019, it does not provide much meaning compare to the Incident column and Incident ID 9 is always missing. Drop it.
# Incident_ID  0.989149 is null
#bus_df.drop(columns=['Incident ID'], inplace=True)

# Direction has dashes, lowercap, uppercap,
# According to the TTC bus readme: 
# The direction of the bus route where B,b or BW indicates both ways. (On an east west route, it includes both east and west)                                           NB - northbound, SB - southbound, EB - eastbound, WB - westbound
# NB - northbound, SB - southbound, EB - eastbound, WB - westbound
# Standardize into N, S, E, W AND B.

'''
bus_df['Direction'] = bus_df['Direction'].apply(lambda x: np.nan if not isinstance(x,str) else x)
all_direction = bus_df['Direction'].unique()

print(bus_df['Direction'].isnull())
print(bus_df.isnull().sum() / bus_df.shape[0])


bus_df[bus_df['Direction'].str.contains(directions,na=False)]

def standard_direction(x):
    if ('N','S','E','W','B') in str(x).upper():
        x = x[0]
    else:
        x = 'NaN'


all_direction = bus_df['Direction'].unique()
directions = ['N','S','E','W','B']
bus_df['Direction'].str.contains('')
bus_df['Direction'] = bus_df['Direction'].apply(lambda x: str(x) if any(direction in str(x).upper() for direction in directions) else np.nan)

    if isinstance(x, str):
        x = x.upper()
        if x.contains('/'):
            x = x.split('/')[0]
    else:
'''
        
# Importdata

streetcar_df = streetcar_df[streetcar_df['Min Delay'].notna()]
subway_df = subway_df[subway_df['Min Delay'].notna()]

# function to remove the leading and trailing white space in the data frame
def trim(dataset):
  # using .strip() to remove the leading and the trailing white spaces in each cell
  trim = lambda x: x.strip() if type(x) is str else x
  return dataset.applymap(trim)

streetcar_df = trim(streetcar_df)
subway_df = trim(subway_df)


streetcar_df = streetcar_df.rename(columns = {'Report Date':'report_date', 'Min Delay': 'min_delay', 'Min Gap':'min_gap', 'Incident ID':'incident_id' })
subway_df = subway_df.rename(columns = {'Date':'report_date', 'Min Delay': 'min_delay', 'Min Gap':'min_gap'})
