# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 12:20:11 2020

@author: Jason Yao
"""

# 2 Data cleaning

# 2.1 Import
import pandas as pd
import numpy as np
from string import punctuation
from datetime import datetime
import re

bus_df = pd.read_csv('./data/merged_bus.csv', encoding='Latin-1')
subway_df = pd.read_csv('./data/merged_subway.csv', encoding='Latin-1')

# 2.2 Cleaning bus dataset
# The columns in this dataset are: Report Date,	Route, Time, Day, Location, Incident, Min Delay, Min Gap, Direction, Vehicle, Min Delay, Incident, ID, Delay, Gap

# 2.2.1 Missing Values
missing_vals_bus = bus_df.isnull().sum() / bus_df.shape[0]
missing_vals_bus[missing_vals_bus > 0].sort_values(ascending=False)

# 2.2.2 Report Date
# Split year, month and day into 3 columns by "-".
bus_df['year'] = bus_df['Report Date'].apply(lambda x: int(x.split('-')[0]))
bus_df['month'] = bus_df['Report Date'].apply(lambda x: int(x.split('-')[1]))
bus_df['day'] = bus_df['Report Date'].apply(lambda x: int(x.split('-')[2]))

# 2.2.3 Route
# According to TTC Routes in Numerical Order: All Time Listing
# https://transittoronto.ca/bus/8108.shtml
# 5-10 are rapid transit route.
# There are no route numbers between 700 to 899.
# 600-699 - Subway/Rapid Transit Routes (discontinued November 2002).

#print(bus_df.Route.unique())
bus_df = bus_df[~((bus_df['Route'] >= 600) & (bus_df['Route'] <900))]
bus_df = bus_df.loc[(bus_df['Route'] >= 5) & (bus_df['Route'] <= 999)]

# 2.2.4 Time
# break down time by hour and min.
# function to convert 12 hour AM/PM to 24 hour clock.
def convert_to_24hour(col):
    in_time = datetime.strptime(col,'%I:%M:%S %p')
    out_time = datetime.strftime(in_time, "%H")
    return out_time

# apply convert_to_24hour function
bus_df['hour'] = bus_df['Time'].apply(convert_to_24hour)
# create a new time by min column
bus_df['min'] = bus_df['Time'].apply(lambda x: int(x.split(':')[1]))

# 2.2.5 Location
# Clean up the location column
# replace punctuations with empty space
bus_df['Location'] = bus_df['Location'].str.upper().str.replace(rf'[{punctuation}]', '')
# rename STC to SCARBOROUGH TOWN CENTRE
bus_df['Location'] = bus_df['Location'].replace(to_replace='STC', value='SCARBOROUGH TOWN CENTRE')
# rename STN to STATION
bus_df['Location'] = bus_df['Location'].replace(to_replace='STN', value='STATION',regex=True)

# if a bus is delayed at a station 1, else 0.
bus_df['at_station'] = bus_df['Location'].apply(lambda x: 1 if 'STATION' in str(x) else 0)

# 2.2.6 Min Delay
# All Min Delay and Delay columns mean the same thing, they are named different.
# They could be merged into one Min Delay column where the NaN rows and the non NaN rows combine together.

bus_df['Min Delay'].fillna(bus_df[' Min Delay'], inplace=True)
bus_df['Min Delay'].fillna(bus_df['Delay'], inplace=True)

# Replace negative time with positive time.
bus_df['Min Delay'] = bus_df['Min Delay'].apply(lambda x: np.abs(x))

# Remove Min delay rows if there's no record of it.
bus_df = bus_df[bus_df['Min Delay'].notna()]

# 2.2.7 Delay type
# create a function to categorize delay time.
# on time is 0 mins delays
# short delay is 1 to 10 mins.
# medium delay is 10 to 30 mins.
# long delay is more than 30 mins.
def delay_type(col):
    if col >= 1 and col <= 10:
        return 'short'
    elif col > 10 and col <= 30:
        return 'medium'
    elif col > 30:
        return 'long'
    elif col == 0:
        return 'on time'

# apply delay_type function
bus_df['delay_type'] = bus_df['Min Delay'].apply(delay_type)

# 2.2.8 Min Gap
# Merge Min Gap and Gap columns into one single column by replacing null values from Min Gap with the Gap column.
bus_df['Min Gap'].fillna(bus_df['Gap'], inplace=True)

# Replace negative time with positive time.
bus_df['Min Gap'] = bus_df['Min Gap'].apply(lambda x: np.abs(x))

# 2.2.9 Direction
# There are about 1000 different records of direction. From numbers to descriptions.
# Example of a description: No damage. No injuries Cleared at 17:24 by cab 107.  1
# Direction has dashes, lowercap, uppercap,
# According to the TTC bus readme:
# The direction of the bus route where B,b or BW indicates both ways. (On an east west route, it includes both east and west)  NB - northbound, SB - southbound, EB - eastbound, WB - westbound
# NB - northbound, SB - southbound, EB - eastbound, WB - westbound
# Standardize into N, S, E, W AND B.

# function to simplify direction in to N,S,E,W,B and NaN for others.
def direction_simplifier(direction):
    # convert all lowercase characters to uppercase, replace punctuations with empty space and remove leading and the trailing spaces.
    direction = str(direction).upper().replace(rf'[{punctuation}]', '').strip()
    if 'NB' in direction or 'NORTH' in direction or 'N\B' in direction or 'N' in direction:
        return 'N'
    elif 'SB' in direction or 'SOUTH' in direction or 'S\B' in direction or 'S' in direction:
        return 'S'
    elif 'EB' in direction or 'EAST' in direction or 'E\B' in direction or 'E' in direction:
        return 'E'
    elif 'WB' in direction or 'WEST' in direction or 'W\B' in direction or 'W' in direction:
        return 'W'
    elif 'BW' in direction or 'BWS' in direction or 'BOTH WAYS' in direction or 'BOTHWAY' in direction or 'BWAYS' in direction or 'B' in direction:
        return 'B'
    else:
        'NaN'

bus_df['direction_simp'] = bus_df['Direction'].apply(direction_simplifier)
bus_df['direction_simp'].value_counts()

# 2.2.10 Incident Id
# Incident ID only occurs on the April 2019 record, it does not provide much meaning compare to the Incident column and Incident ID 9 is always missing.
# Drop it.
# Incident_ID has 99% null value

# Drop duplicate columns  Min Delay, Delay, Gap and Incident ID
bus_df.drop(columns=[' Min Delay', 'Delay','Gap','Incident ID'], inplace=True)

# 2.2.11 Trim data frame
# By: ImportData
# function to remove the leading and trailing white space in the data frame
def trim(dataset):
  # using .strip() to remove the leading and the trailing white spaces in each cell
  trim = lambda x: x.strip() if type(x) is str else x
  return dataset.applymap(trim)

bus_df = trim(bus_df)

# 2.2.12 Make all column names lowercase so thet are easier to work with.
bus_df = bus_df.rename(columns = {'Report Date':'exact_date', 'Route':'route_num', 'Time':'exact_time','Day':'day_of_week','Location':'location', 'Incident':'incident','Direction':'direction',
                                  'Vehicle':'vehicle','Min Delay': 'delay_min', 'Min Gap':'gap_min' })

# 2.3 Cleaning Subway dataset
# The columns in this dataset are: Date, Time, Day, Station, Code, Min Delay, Min Gap, Bound, Line, Vehicle

# 2.3.1 Missing Value
missing_vals_subway = subway_df.isnull().sum() / subway_df.shape[0]
missing_vals_subway[missing_vals_subway > 0].sort_values(ascending=False)

# 2.3.2 Date
subway_df['year'] = subway_df['Date'].apply(lambda x: int(x.split('-')[0]))
subway_df['month'] = subway_df['Date'].apply(lambda x: int(x.split('-')[1]))
subway_df['day'] = subway_df['Date'].apply(lambda x: int(x.split('-')[2]))

# 2.3.3 Time
subway_df['hour'] = subway_df['Time'].apply(convert_to_24hour)
subway_df['min'] = subway_df['Time'].apply(lambda x: int(x.split(':')[1]))

# sort subway data by Date and Time
subway_df.sort_values(['Date','Time'], inplace=True)

# 2.3.4 Station 
# From 608 different inputs to 75 stations
# this function is to clean up the station column
def clean_station_col(text):
    text = re.sub(rf'[{punctuation}]', '',text) # Remove punctuation
    text = re.sub('\s+(BD|SRT|YUS|YU)+\s',' ',text) # Remove BD, SRT,YU,YUS
    text = re.sub('CTR','CENTRE',text) # Replace ctr with centre
    text = re.sub('(SATATIO|STAITON|STATI|CAR HOUSE|STN|STATIO|YARD|WYE|HOSTLER|CARHOUSE|SHOP|SHOPS|LOWER|COMMERCE|HOSTLE)+$',' STATION',text) # Replace texts not end with station to station
    # split by (, TO, AND and only the words before them
    text = text.split('(')[0]
    text = text.split(' TO ')[0]
    text = text.split(' AND ')[0]
    if 'YONGEUNIVERSITY' in text or 'YONGE UNIVERSITY' in text:
        text = 'YONGE UNIVERSITY LINE'
    if  not text.endswith('LINE') and not text.endswith('SUBWAY') and 'STATION' not in text:
        text = text + ' STATION'
    if 'SCARB' in text:
        text = 'SCARBOROUGH CENTRE STATION'
    if 'DAVISVILLE' in text:
        text = 'DAVISVILLE STATION'
    if 'GREENWOOD' in text:
        text = 'GREENWOOD STATION'
    if 'KEELE' in text:
        text = 'KEELE STATION'
    if 'MCCOWAN' in text:
        text = 'MCCOWAN STATION'
    if 'WILSON' in text:
        text = 'WILSON STATION'
    return text

subway_df['Station'] = subway_df['Station'].apply(clean_station_col)

subway_df['Station'] = subway_df['Station'].apply(clean_station_col)


# a list of station
station_list = ['BATHURST',
'BAY',
'BAYVIEW',
'BESSARION',
'BLOOR',
'BROADVIEW',
'CASTLE FRANK',
'CHESTER',
'CHRISTIE',
'COLLEGE',
'COXWELL',
'DAVISVILLE',
'DON MILLS',
'DONLANDS',
'DOWNSVIEW PARK',
'DUFFERIN',
'DUNDAS',
'DUNDAS WEST',
'DUPONT',
'EGLINTON',
'EGLINTON WEST',
'ELLESMERE',
'FINCH',
'FINCH WEST',
'GLENCAIRN',
'GREENWOOD',
'HIGH PARK',
'HIGHWAY 407',
'ISLINGTON',
'JANE',
'KEELE',
'KENNEDY',
'KING',
'KIPLING',
'LANSDOWNE',
'LAWRENCE',
'LAWRENCE EAST',
'LAWRENCE WEST',
'LESLIE',
'MAIN STREET',
'MCCOWAN',
'MIDLAND',
'MUSEUM',
'NORTH YORK CENTRE',
'OLD MILL',
'OSGOODE',
'OSSINGTON',
'PAPE',
'PIONEER VILLAGE',
'QUEEN',
"QUEEN'S PARK",
'ROSEDALE',
'ROYAL YORK',
'RUNNYMEDE',
'SCARBOROUGH CENTRE',
'SHEPPARD WEST',
'SHEPPARD',
'SHERBOURNE',
'SPADINA',
'ST CLAIR',
'ST CLAIR WEST',
'ST ANDREW',
'ST GEORGE',
'ST PATRICK',
'SUMMERHILL',
'UNION',
'VAUGHAN METRO CENTRE',
'VAUGHAN MC',
'VICTORIA PARK',
'WARDEN',
'WELLESLEY',
'WILSON',
'WOODBINE',
'YORK MILLS',
'YORK UNIVERSITY',
'YORKDALE',
'YONGE',
'QUEENS PARK',
'SCAR',
'SHP',
'NORTH YORK CTR'
]

# create regex pattern out of the list of words
station_list_comb = '|'.join(station_list)
# remove rows from the subway dataset if they don't contain any stations from the station list
subway_df = subway_df[subway_df['Station'].str.contains(station_list_comb)]
#print(station_list_comb)

# remove noisy station names where they have less than 10 delays
# only removed 1% of data 
subway_df = subway_df[subway_df.groupby(['Station'])['Date'].transform('count') > 10]

# clean up station column for specific 
subway_df['Station'] = subway_df['Station'].replace(dict.fromkeys(['BLOOR STATION','YONGE STATION'],'BLOOR YONGE STATION'))
subway_df['Station'] = subway_df['Station'].replace(dict.fromkeys(['SHEPPARDYONGE STATION','SHEPPARD STATION','SHEPPARD-YONGE STATION','YONGE SHEP STATION','YONGE SHP STATION'],'SHEPPARD YONGE STATION'),regex=True)

# 2.3.5 at_station
# if a subway train is delayed at a station
subway_df['at_station'] = subway_df['Station'].apply(lambda x: 1 if 'STATION' in x else 0)
# at interchange station

# 2.3.6 Bound
# In this case, bound is direction.
subway_df.Bound = subway_df.Bound.replace({'Y':np.nan,'5':np.nan,'R':np.nan})

# 2.3.7 Line
# function to simplify subway lines
def line_simplifier(line):
    line = str(line).upper().replace(rf'[{punctuation}]', '').strip()
    if 'YU  BD' in line or 'YUBD' in line or 'YU BD' in line or 'BDYU' in line:
        return 'YU-BD'
    elif 'BD' in line or 'BLOOR DANFORTH LINE' in line or 'BLOOR DANFORTH LINES' in line or 'BLOORDANFORTH' in line:
        return 'BD'
    elif 'YU' in line or 'YU LINE' in line :
        return 'YU'
    elif 'SRT' in line:
        return 'SRT'
    elif 'SHP' in line or 'SHEPPARD' in line:
        return 'SHP'
    else:
        'NaN'

subway_df['line_simp'] = subway_df['Line'].apply(line_simplifier)
subway_df.line_simp = subway_df.line_simp.replace({'YU-BD':np.nan})
subway_df['line_simp'].value_counts()

# 2.3.8 Min Delay
# drop null values
subway_df = subway_df[subway_df['Min Delay'].notna()]

# 2.3.9 categorize delay into on-time, short, medium and long
subway_df['delay_type'] = subway_df['Min Delay'].apply(delay_type)

# 2.3.10 trim dataset
subway_df = trim(subway_df)

# 2.3.11 rename columns
subway_df = subway_df.rename(columns = {'Date':'exact_date', 'Time':'exact_time','Day':'day_of_week','Station':'station','Code':'code','Bound':'bound','Line':'line','Vehicle':'vehicle', 'Min Delay': 'delay_min', 'Min Gap':'gap_min'})

# 2.4 Save to csv
# save both dataframes to 2 new csv files
bus_df.to_csv('./data/bus_cleaned.csv',index = False)
subway_df.to_csv('./data/subway_cleaned.csv',index = False)
