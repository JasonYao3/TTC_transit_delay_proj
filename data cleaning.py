# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 12:20:11 2020

@author: Jason
"""

import pandas as pd

bus_df = pd.read_csv('./data/merged_bus.csv', encoding='Latin-1')
subway_df = pd.read_csv('./data/merged_subway.csv', encoding='Latin-1')
streetcar_df = pd.read_csv('./data/merged_streetcar.csv', encoding='Latin-1')

# bus data cleaning

# Report Date -> Report_Date
# Split year, month and day into 3 columns by "-"
bus_df = bus_df['Report Date']
# Time - split by hour and min.

# Day - rename to short form

# Route:
# !00 Flemington Route -> Flemington Route

# Min Delay: negative not sure what that means, 0 means 0 min delay and NaN means no record
# All Min Delay and Delay columns mean the same thing, they are just name different. They could be merged into one Min Delay column where the NaN rows and the non NaN rows combine together

# Same thing goes to the Min Gap and Gap column. Merge them together into one column

# Incident ID only occurs on April 2019, it does not provide much meaning compare to the Incident column and Incident ID 9 is always missing. Drop it.
# Incident_ID  0.989149 is null


# Direction has dashes, lowercap, uppercap,
# According to the TTC bus readme: 
# The direction of the bus route where B,b or BW indicates both ways. (On an east west route, it includes both east and west)                                           NB - northbound, SB - southbound, EB - eastbound, WB - westbound
# NB - northbound, SB - southbound, EB - eastbound, WB - westbound
# Standardize into N, S, E, W AND B.

# Remove min delay and Min Gap rows if NaN