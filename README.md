# TTC Bus and Subway Delay Data Analysis: Project Overview
* 
* Merged 46 excels files from City of Toronto using python
* Engineered features from the text of each ...
* Explored datasets to analyze relationships among features (both continuous and categorical)
* Optimized Linear, Lasso, and Random Forest Regressors using GridsearchCV to reach the best model. 
* Built a client facing API using flask 

## Code and Resources Used 
**Python Version:** 3.7  
**Packages:** pandas, numpy, matplotlib, seaborn 
**Data Source:**  https://open.toronto.ca/
**Ken Jee:** https://github.com/PlayingNumbers/ds_salary_proj

## Intro
* As a student who went to Ryerson University, I had to commute alot on the TTC buses and subways every week. During my riderships, I had experienced countless numbers of delays on both bus and subway, whether they were long or short delays. Now, I think it would be interesting to dive into the delay data and try to find out interesting insights.

## Data Collection
* I downloaded the data from the City of Toronto’s Open Data Portal https://open.toronto.ca/. There are two sets of data for the two different transportations from January 1, 2014 to May 31, 2020.
* The TTC bus dataset has 7 excel files with 12 excel worksheets for each month from 2014 to 2019 and 5 excel worksheets for each month in 2020.
* The TTC subway dataset has 39 excel files for each month from 2014 to 2020.
* In the dataset, we got the following:
*	Report 
*  Date	
*  Route	
*  Time	
*  Day	
*  Location	
*  Incident	
*  Min Delay	
*  Min Gap	
*  Direction	
*  Vehicle
*  Station	
*  Code	
*  Bound	
*  Line

## Data Cleaning
In the 1.Merge_excel IPython file, I merged the excel files for each transit into two merged excel files.
In the 2.Data cleaning Python file, I needed to clean it up the two merged excel files so that it was usable for our analysis. I made the following changes and created the following variables:

*	Parsed date into year, month and date and time into hour and minute.
*	Removed route numbers that are not bus route numbers
*	Converted time from 12 hour to 24 hour
*  Cleaned up location 
*	Removed rows without delay
*  Made a new column for bus delay at station
*  Removed duplicate columns and fill in NULL values
*  Added a column for different delay type
*  Standardized direction and subway line column

## EDA
In the 3.Bus EDA and 4.Subway EDA IPython files. 
* I looked at the distributions of the continuous variables using seaborn graphs(distplot and boxplot)  the relationships using heatmap and the statistics measure using numpy quantiles function
* I looked at the value counts for the various categorical variables using seaborn barplots and countplots for the Top 20's.
* I used barplots to show the relationship between delays by days of the week and different direction.
* I used wordclouds to show the most frequent words in the location and station columns.
Below are a few highlights from the graphs. 

![alt text](")
![alt text](")
![alt text](")

## Model Building 
 
I tried three different models:
*	**Multiple Linear Regression** – Baseline for the model
*	**Lasso Regression** – Because of the sparse data from the many categorical variables, I thought a normalized regression like lasso would be effective.
*	**Random Forest** – Again, with the sparsity associated with the data, I thought that this would be a good fit. 

## Model performance
The Random Forest model far outperformed the other approaches on the test and validation sets. 
*	**Random Forest** : MAE =
*	**Linear Regression**: MAE = 
*	**Ridge Regression**: MAE = 

## Productionization 
In this step, I built a flask API endpoint that was hosted on a local webserver by following along with the TDS tutorial in the reference section above. The API endpoint takes in a request with a list of values from a job listing and returns an estimated salary. 


