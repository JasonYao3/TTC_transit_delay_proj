# TTC Bus and Subway Delay Data Analysis: Project Overview
* Performed extensive data analysis on TTC bus and subway delays to see what caused delay and when it happened. 
* Merged and cleaned 46 excels files, for over 600k records of transit delays from City of Toronto.
* Engineered variables features from each column.
* Explored datasets to analyze relationships among features (both continuous and categorical).

## Table of Contents
<details open>
<summary>Show/Hide</summary>
<br>

1. [ Summary of Findings ](#Summary_of_Findings)
2. [ Introduction ](#Introduction)    
3. [ Data Collection ](#Data_Collection)
4. [ Data Merging ](#Data_Merging)
5. [ Data Cleaning ](#Data_Cleaning)
6. [ EDA ](#EDA)
</details>

<a name="Summary_of_Findings"></a>
## Summary of Findings
*
*

<a name="Introduction"></a>
## Introduction

As a student who went to Ryerson University, I had to commute almost every week on TTC buses and subways. During my riderships, I had experienced countless number of delays on both buses and subwayes, whether they were long delays (on a shuttle bus) or short delays. Now, I think it would be interesting to dive into the delay data and try to find interesting insights out of it.

<a name="Data_Collection"></a>
## Data Collection
I downloaded the data from the [City of Toronto’s Open Data Portal](https://open.toronto.ca/). There are two sets of data for the two different transportations from January 1, 2014 to May 31, 2020.
The TTC bus dataset has 7 excel files with 12 excel worksheets for each month from 2014 to 2019 and 5 excel worksheets for each month in 2020.
The TTC subway dataset has 39 excel files for each month from 2014 to 2020.

In the dataset, each row is a record of the delay-causing incident and we have the following information:
*  Report date
*  Route Number (The number of the bus route)
*  Time of the day	
*  Day	
*  Location	/ Station (The location or station of the delay-causing incident)
*  Incident (The description of the delay-causing incident)
*  Delay (in minute)	
*  Min Gap (in minute)
*  Direction / Bound (where the vehicle heading)
*  Vehicle (vehicle number)
*  Code	(TTC delay code)
*  Line (TTC subway Line)

<a name="Data_Merging"></a>
## Data Merging
In the 1.Merge_excel IPython file, I merged all excel files for each transit into two separate excel files using the following merge excel function.

<details open>
<summary>Show/Hide</summary>
<br>
    
```
# This function merges all excel files and return a dataframe
def merge_excel(transit):
    transit=str(transit)
    path = os.path.abspath('../data/%s'%transit)
    file = os.listdir(path)
    file_list = [os.path.join(path,file) for file in os.listdir(path)]
    df_total = pd.DataFrame()
    for file in file_list:
        excel_file = pd.ExcelFile(file)
        sheets = excel_file.sheet_names
        for sheet in sheets:
            df = excel_file.parse(sheet_name = sheet)
            df_total = df_total.append(df)
    return df_total
```
</details>

<a name="Data_Cleaning"></a>
## Data Cleaning
In the 2.Data cleaning Python file, I needed to clean it up the two merged excel files so that they are usable for our analysis. I made the following changes and created the following variables:

Parsed date into year, month and date and time into hour and minute.

```
bus_df['year'] = bus_df['Report Date'].apply(lambda x: int(x.split('-')[0]))
bus_df['month'] = bus_df['Report Date'].apply(lambda x: int(x.split('-')[1]))
bus_df['day'] = bus_df['Report Date'].apply(lambda x: int(x.split('-')[2]))
```

Removed route numbers that are not bus route numbers. According to [TTC ROUTES IN NUMERICAL ORDER: ALL TIME LISTING](https://transittoronto.ca/bus/8108.shtml)

```
bus_df = bus_df[~((bus_df['Route'] >= 600) & (bus_df['Route'] <900))]
bus_df = bus_df.loc[(bus_df['Route'] >= 5) & (bus_df['Route'] <= 999)]
```

Converted time from 12 hour to 24 hour.

```
def convert_to_24hour(col):
    in_time = datetime.strptime(col,'%I:%M:%S %p')
    out_time = datetime.strftime(in_time, "%H")
    return out_time
bus_df['hour'] = bus_df['Time'].apply(convert_to_24hour)
```

Cleaned up location and station.

```
bus_df['Location'] = bus_df['Location'].str.upper().str.replace(rf'[{punctuation}]', '')
bus_df['Location'] = bus_df['Location'].replace(to_replace='STC', value='SCARBOROUGH TOWN CENTRE')
bus_df['Location'] = bus_df['Location'].replace(to_replace='STN', value='STATION',regex=True)
```

Removed empty delay rows.

```
bus_df = bus_df[bus_df['Min Delay'].notna()]
```

Made a new column for whether transit delayed at station or not
 
```
bus_df['at_station'] = bus_df['Location'].apply(lambda x: 1 if 'STATION' in str(x) else 0)
```

Removed duplicate columns and fill in NULL values for delay and gap columns.

```
bus_df['Min Delay'].fillna(bus_df[' Min Delay'], inplace=True)
bus_df['Min Delay'].fillna(bus_df['Delay'], inplace=True)
bus_df['Min Gap'].fillna(bus_df['Gap'], inplace=True)
bus_df.drop(columns=[' Min Delay', 'Delay','Gap'], inplace=True)
```

Added a new column to categorize different delay type by how long it is.

<details open>
<summary>Show/Hide</summary>
<br>
    
```
def delay_type(col):
    if col >= 1 and col <= 10:
        return 'short'
    elif col > 10 and col <= 30:
        return 'medium'
    elif col > 30:
        return 'long'
    elif col == 0:
        return 'on time'
 bus_df['delay_type'] = bus_df['Min Delay'].apply(delay_type)
```
</details>
Standardized transits direction and subway line column.

<details open>
<summary>Show/Hide</summary>
<br>
    
```
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
```
</details>

<a name="EDA"></a>
## EDA
In the 3.Bus EDA and 4.Subway EDA IPython files. 

-  I looked at the distributions of the continuous variables using seaborn graphs(distplot and boxplot)

<h5 align="center"> Distribution plot and box plot of delay for bus and subway ( Bus (Left) and Subway (Right) )</h5>
<table><tr><td><img src='https://github.com/JasonYao3/TTC_transit_delay_proj/blob/master/pictures/bus_delay_min_dist.jpg' width=500></td><td><img src='https://github.com/JasonYao3/TTC_transit_delay_proj/blob/master/pictures/subway_delay_min_dist.jpg' width=500></td></tr></table>

- Both graphs have many outliers.
- The bus graph on the left has 456000 outliers and 10 minutes delay has 67000 records.
- The subway graph on the right has 113000 outliers and 0 minute delay has 78000 records.
    
```
# initialize continuous variables
bus_cont = bus_df[['route_num','vehicle','year','month','day','hour','min','delay_min','gap_min']]
# Using a for loop to plot each continous variables and compute quantiles.
for col in bus_cont.columns:
    fig, ax = plt.subplots(1,2, figsize=(12,5))
    cont_num = bus_cont[col].value_counts()
    chart = sns.distplot(cont_num, ax=ax[0], color="orangered", kde=True)
    ax[0].set_title("Graph for %s: total categories = %d" %(col, len(cont_num)))
    sns.boxplot(cont_num, ax=ax[1], color="orangered")
    plt.show()

    compute_quantiles(cont_num)
    print('\n')
```

- check correlations between continuous variables using heatmap

<img src='https://github.com/JasonYao3/TTC_transit_delay_proj/blob/master/pictures/bus_heatmap.jpg' width=500>

```
# check correlations between continuous variables
cmap = sns.diverging_palette(660, 600, as_cmap=True)
sns.heatmap(bus_cont.corr(), vmax=.3, center=0, cmap=cmap, square=True, linewidths=.5, cbar_kws={"shrink": .5})
```

- Calculate quantiles, Interquartile range and outliers using numpy quantiles function

```
# a function to find quantiles, or where most data are.
def compute_quantiles(col_counts):
    Q1 =  np.quantile(col_counts, 0.25)
    Q3 =  np.quantile(col_counts, 0.75)
    IQR = Q3 - Q1
    print('Most data are within %d to %d.'%(Q1,Q3))
    print('Median is', np.quantile(col_counts, 0.5))
    print('The data are usually below %d.'%np.quantile(col_counts, 0.95))
    
    lower_fence = Q1 - 1.5 * (IQR)
    upper_fence = Q3  + 1.5 * (IQR)
    outlier = col_counts[col_counts < lower_fence].sum() + col_counts[col_counts > upper_fence].sum()
    print('Anything above %d and below %d is an outlier.'%(upper_fence,lower_fence))
    print("There are %d outliers." %outlier)
    print('Maximum occurence is %d of %s.' %(col_counts.max(), col_counts.index[0]))
compute_quantiles(bus_date_counts)
```

- I looked at the value counts for the various categorical variables using seaborn barplots and countplots for top code, subway station, bus location and bus route.

<h5 align="center"> Bar graphs for bus and subway delay by hour of the day ( Bus (Left) and Subway (Right) )</h5>
<table><tr><td><img src='https://github.com/JasonYao3/TTC_transit_delay_proj/blob/master/pictures/bus_hour_bargraph.jpg' width=500></td><td><img src='https://github.com/JasonYao3/TTC_transit_delay_proj/blob/master/pictures/subway_hour_bargraph.jpg' width=500></td></tr></table>
    
```
# dataframe for categorical variables
bus_cat = bus_df[['year','month','day','hour','day_of_week', 'incident', 'at_station', 'direction_simp', 'delay_type']]

# Using a for loop to plot each categorical variable.
for col in bus_cat.columns:
    plt.figure(figsize=(12,5))
    cat_num = bus_cat[col].value_counts()
    print("Graph for %s: total categories = %d" %(col, len(cat_num)))
    chart = sns.barplot(x=cat_num.index, y=cat_num,color="lightseagreen")
    chart.set_xticklabels(chart.get_xticklabels(), rotation=20, horizontalalignment='right')
    plt.ylabel("")
    plt.xlabel(col)
    plt.title("Graph for %s" %(col))
    plt.show()
```

- Use barplots to show the relationship between delays vs day of the week, incident, hour, direction, subway lines.

<h5 align="center"> Delays by Days of the Week and Subway Lines (Bus Direction) ( Bus Direction(Left) and Subway Lines (Right) )</h5>
<table><tr><td><img src='https://github.com/JasonYao3/TTC_transit_delay_proj/blob/master/pictures/Delays%20vs%20Days%20of%20the%20Week%20and%20Direction.JPG' width=500></td><td><img src='https://github.com/JasonYao3/TTC_transit_delay_proj/blob/master/pictures/Delays%20by%20Days%20of%20the%20Week%20and%20Subway%20Lines.JPG' width=500></td></tr></table>

```
plt.figure(figsize=(12,5));
sns.barplot(x='day_of_week', y='delay_min', data= bus_df, ci=None);
plt.title("Delays vs Day of the Week");
plt.xlabel("Days of the Week");
plt.ylabel("Delay in minute");
```

- Use wordclouds to show the most frequent bus location and subway station.

<h5 align="center"> Wordcloud to visualize most frequent location and station ( Bus Location (Left) and Subway Station (Right) )</h5>
<table><tr><td><img src='https://github.com/JasonYao3/TTC_transit_delay_proj/blob/master/pictures/bus_location_wordcloud.jpg' width=500></td><td><img src='https://github.com/JasonYao3/TTC_transit_delay_proj/blob/master/pictures/subway_station_wordcloud.jpg' width=500></td></tr></table>

```
# Code is from Ken Jee
words = " ".join(bus_df_notna['location'])

def punctuation_stop(text):
    """remove punctuation and stop words"""
    filtered = []
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text)
    for w in word_tokens:
        if w not in stop_words and w.isalpha():
            filtered.append(w.lower())
    return filtered


words_filtered = punctuation_stop(words)

text = " ".join([ele for ele in words_filtered]) 

wc= WordCloud(background_color="white", random_state=1,stopwords=STOPWORDS, max_words = 2000, width =1500, height = 800)
wc.generate(text)

plt.figure(figsize=[10,10])
plt.imshow(wc, interpolation="bilinear")
plt.axis('off')
plt.show()
```

### What Next?
Model building, model performance, and use flask to productionize. 


