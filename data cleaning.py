# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 12:20:11 2020

@author: Jason Yao
"""

import pandas as pd
import numpy as np

bus_df = pd.read_csv('./data/merged_bus.csv', encoding='Latin-1')
streetcar_df = pd.read_csv('./data/merged_streetcar.csv', encoding='Latin-1')
subway_df = pd.read_csv('./data/merged_subway.csv', encoding='Latin-1')

# Bus 

# Missing Values
missing_vals_bus = bus_df.isnull().sum() / bus_df.shape[0]
missing_vals_bus[missing_vals_bus > 0].sort_values(ascending=False)

# Report Date column: Split year, month and day into 3 columns by "-"



bus_df['report_year'] = bus_df['Report Date'].apply(lambda x: int(x.split('-')[0]))
bus_df['report_month'] = bus_df['Report Date'].apply(lambda x: int(x.split('-')[1]))
bus_df['report_day'] = bus_df['Report Date'].apply(lambda x: int(x.split('-')[2]))

# Route
# According to TTC Routes in Numerical Order: All Time Listing
# https://transittoronto.ca/bus/8108.shtml
# 5-10 will be renumbered as rapid transit routes need them
# There is no route number between 700 to 899
# 600-699 - Subway/Rapid Transit Routes (discontinued November 2002)

#print(bus_df.Route.unique())
bus_df = bus_df[~((bus_df['Route'] >= 600) & (bus_df['Route'] <900))]
bus_df = bus_df.loc[(bus_df['Route'] >= 5) & (bus_df['Route'] <= 999)]

# Time - break down by hour and min.
bus_df['time_hour'] = bus_df['Time'].apply(lambda x: int(x.split(':')[0]))
bus_df['time_min'] = bus_df['Time'].apply(lambda x: int(x.split(':')[1]))

# Location
bus_df['Location'] = bus_df['Location'].str.upper()
bus_df['Location'] = bus_df['Location'].replace(to_replace='STC', value='SCARBOROUGH TOWN CENTRE')
bus_df['Location'] = bus_df['Location'].replace(to_replace='STN', value='STATION',regex=True)


# Min Delay: negative not sure what that means, 0 means 0 min delay and NaN means no record
# All Min Delay and Delay columns mean the same thing, they are just name different. They could be merged into one Min Delay column where the NaN rows and the non NaN rows combine together

bus_df['Min Delay'].fillna(bus_df[' Min Delay'], inplace=True)
bus_df['Min Delay'].fillna(bus_df['Delay'], inplace=True)

# Negative time 
bus_df['Min Delay'] = bus_df['Min Delay'].apply(lambda x: np.abs(x))

# function to categorize delay time
def delay_type(col):
    if col >= 0 and col <= 10:
        return 'short'
    elif col > 10 and col <= 30:
        return 'medium'
    elif col > 30:
        return 'long'
    
bus_df['delay_type'] = bus_df['Min Delay'].apply(delay_type)

# Min Gap
bus_df['Min Gap'].fillna(bus_df['Gap'], inplace=True)

# Replace negative time with absolute value of it
bus_df['Min Gap'] = bus_df['Min Gap'].apply(lambda x: np.abs(x))

# Direction
# There are about 1000 different records of direction. From numbers to descriptions.
# Example of a description: No damage. No injuries Cleared at 17:24 by cab 107.                           1
# bus_df['Direction'] = bus_df['Direction'].str.upper()
# Direction has dashes, lowercap, uppercap,
# According to the TTC bus readme: 
# The direction of the bus route where B,b or BW indicates both ways. (On an east west route, it includes both east and west)                                           NB - northbound, SB - southbound, EB - eastbound, WB - westbound
# NB - northbound, SB - southbound, EB - eastbound, WB - westbound
# Standardize into N, S, E, W AND B.


# Incident Id
# Incident ID only occurs on April 2019, it does not provide much meaning compare to the Incident column and Incident ID 9 is always missing. Drop it.
# Incident_ID  0.989149 is null

# Drop duplicate columns  Min Delay, Delay, Gap and Incident ID
bus_df.drop(columns=[' Min Delay', 'Delay','Gap','Incident ID'], inplace=True)

# Remove Min delay rows if NaN
bus_df = bus_df[bus_df['Min Delay'].notna()]

# By: ImportData 
# function to remove the leading and trailing white space in the data frame
def trim(dataset):
  # using .strip() to remove the leading and the trailing white spaces in each cell
  trim = lambda x: x.strip() if type(x) is str else x
  return dataset.applymap(trim)

bus_df = trim(bus_df)

# Rename columns
bus_df = bus_df.rename(columns = {'Report Date':'report_date', 'Min Delay': 'delay_min', 'Min Gap':'gap_min' })

# Street Car

# Missing value
missing_vals_streetcar = streetcar_df.isnull().sum() / streetcar_df.shape[0]
missing_vals_streetcar[missing_vals_streetcar > 0].sort_values(ascending=False)

# Report Date
streetcar_df['report_year'] = streetcar_df['Report Date'].apply(lambda x: int(x.split('-')[0]))
streetcar_df['report_month'] = streetcar_df['Report Date'].apply(lambda x: int(x.split('-')[1]))
streetcar_df['report_day'] = streetcar_df['Report Date'].apply(lambda x: int(x.split('-')[2]))

# Time
streetcar_df['time_hour'] = streetcar_df['Time'].apply(lambda x: int(x.split(':')[0]))
streetcar_df['time_min'] = streetcar_df['Time'].apply(lambda x: int(x.split(':')[1]))

# Route
# 300-399 - Routes in the overnight “Blue Night Network”
# 500-599 - Streetcar routes
streetcar_df = streetcar_df[((streetcar_df['Route'] > 300) & (streetcar_df['Route'] < 400)) | ((streetcar_df['Route'] >= 500) & (streetcar_df['Route'] <600)) ]

# Location
streetcar_df['Location'] = streetcar_df['Location'].str.upper()

# Min Delay
streetcar_df['Min Delay'].fillna(streetcar_df['Delay'], inplace=True)

# Negative time 
streetcar_df['Min Delay'] = streetcar_df['Min Delay'].apply(lambda x: np.abs(x))

# categorize delay
streetcar_df['delay_type'] = streetcar_df['Min Delay'].apply(delay_type)


# Min Gap
streetcar_df['Min Gap'].fillna(streetcar_df['Gap'], inplace=True)

# Drop duplicate columns
streetcar_df.drop(columns=['Delay','Gap'], inplace=True)


streetcar_df = streetcar_df[streetcar_df['Min Delay'].notna()]

streetcar_df = trim(streetcar_df)

# Rename columns
streetcar_df = streetcar_df.rename(columns = {'Report Date':'report_date', 'Min Delay': 'delay_min', 'Min Gap':'gap_min', 'Incident ID':'incident_id' })

# Subway

# Missing Value
missing_vals_subway = subway_df.isnull().sum() / subway_df.shape[0]
missing_vals_subway[missing_vals_subway > 0].sort_values(ascending=False)

# Date
subway_df['report_year'] = subway_df['Date'].apply(lambda x: int(x.split('-')[0]))
subway_df['report_month'] = subway_df['Date'].apply(lambda x: int(x.split('-')[1]))
subway_df['report_day'] = subway_df['Date'].apply(lambda x: int(x.split('-')[2]))

# Time
subway_df['time_hour'] = subway_df['Time'].apply(lambda x: int(x.split(':')[0]))
subway_df['time_min'] = subway_df['Time'].apply(lambda x: int(x.split(':')[1]))

# parse station
subway_df['is_station'] = subway_df['Station'].apply(lambda x: 1 if 'STATION' in x else 0)

# drop null values 
subway_df = subway_df[subway_df['Min Delay'].notna()]

# categorize delay
subway_df['delay_type'] = subway_df['Min Delay'].apply(delay_type)

# trim
subway_df = trim(subway_df)

# rename columns
subway_df = subway_df.rename(columns = {'Date':'report_date', 'Min Delay': 'delay_min', 'Min Gap':'gap_min'})

# save all 3 dataframes to 3 new csv files
bus_df.to_csv('./data/bus_cleaned.csv',index = False)
streetcar_df.to_csv('./data/streetcar_cleaned.csv',index = False)
subway_df.to_csv('./data/subway_cleaned.csv',index = False)