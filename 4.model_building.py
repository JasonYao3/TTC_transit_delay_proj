# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 17:02:26 2020

@author: Jason
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_absolute_error

df = pd.read_csv('./data/subway_cleaned.csv')

# choose relevant columns
df.columns

df_model = df[['Code','delay_min','Bound','line_simp','report_year','report_month','report_day','time_hour','time_min','delay_type','at_station']]

# get dummy data
df_dum = pd.get_dummies(df_model)

# train test split
X = df_dum.drop('delay_min', axis=1)
y = df_dum.delay_min.values

# 80 percent in train set, 20 percent in test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# multiple linear regression
# P>|t| < 0.05 (5%) is relevant
X_sm = X = sm.add_constant(X)
model = sm.OLS(y, X_sm)
#print(model.fit().summary())

lm = LinearRegression()
lm.fit(X_train, y_train)

print(np.mean(cross_val_score(lm, X_train, y_train, scoring='neg_mean_absolute_error', cv=3)))

# lasso regression
#lm_l = Lasso(alpha= ) best alpha
lm_l = Lasso()
lm_l.fit(X_train,y_train)
print(np.mean(cross_val_score(lm_l, X_train, y_train, scoring='neg_mean_absolute_error', cv=3)))

alpha = []
error = []
for i in range(1, 100):
    alpha.append(i/100)
    lml = Lasso(alpha=(i/100))
    error.append(np.mean(cross_val_score(lm_l, X_train, y_train, scoring='neg_mean_absolute_error', cv=3)))
    
#plt.plot(alpha,error)

err = tuple(zip(alpha, error))
df_err = pd.DataFrame(err, columns = ['alpha','error'])
df_err[df_err.error == max(df_err.error)]

# random forest
rf = RandomForestRegressor()

print(np.mean(cross_val_score(rf, X_train, y_train, scoring='neg_mean_absolute_error', cv=3)))

# tune model GridsearchCV
parameters = {'n_estimators':range(10,300,10), 'Criterion':('mse','mae'), 'max_features':('auto','sqrt','Log2')}

gs = GridSearchCV(rf, parameters,scoring='neg_mean_absolute_error',cv=3)
gs.fit(X_train,y_train)

gs.best_score_
gs.best_estimator_

# test ensembles
tpred_lm = lm.predict(X_test)
tpred_lml = lm_l.predict(X_test)
tpred_rf = gs.best_estimator_.predict(X_test)

mean_absolute_error(y_test, tpred_lm)
mean_absolute_error(y_test, tpred_lml)
mean_absolute_error(y_test, tpred_rf)

mean_absolute_error(y_test,(tpred_lm+tpred_rf)/2)