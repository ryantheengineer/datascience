# -*- coding: utf-8 -*-
"""
Created on Tue May 16 08:35:16 2023

@author: Ryan.Larson

Working through Kaggle time series tutorials.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from warnings import simplefilter

##############################
##### BOOK SALES EXAMPLE #####
##############################

# df = pd.read_csv(
#     "book_sales.csv",
#     index_col='Date',
#     parse_dates=['Date'],
# ).drop('Paperback', axis=1)

# df['Time'] = np.arange(len(df.index))

# plt.style.use("seaborn-whitegrid")
# plt.rc(
#         "figure",
#         autolayout=True,
#         figsize=(11, 4),
#         titlesize=18,
#         titleweight='bold',
# )
# plt.rc(
#         "axes",
#         labelweight="bold",
#         labelsize="large",
#         titleweight="bold",
#         titlesize=16,
#         titlepad=10,
# )

# fig, ax = plt.subplots()
# ax.plot('Time', 'Hardcover', data=df, color='0.75')
# ax = sns.regplot(x='Time', y='Hardcover', data=df, ci=None, scatter_kws=dict(color='0.25'))
# ax.set_title('Time Plot of Hardcover Sales');

# # Add lag features (we can regress on lag features to fit curves to lag plots
# # where each observation in a series is plotted against the previous observation)
# df['Lag_1'] = df['Hardcover'].shift(1)
# df = df.reindex(columns=['Hardcover', 'Lag_1'])

# # The plot created in the following section shows that sales on one day (Hardcover)
# # are correlated with sales from the previous day (Lag_1).
# # Lag features let you model serial dependence, when an observation can be
# # predicted from previous observations.
# # Adapting machine learning algorithms to time series problems is largely about
# # feature engineering with the time index and lags.
# fig, ax = plt.subplots()
# ax = sns.regplot(x='Lag_1', y='Hardcover', data=df, ci=None, scatter_kws=dict(color='0.25'))
# ax.set_aspect('equal')
# ax.set_title('Lag Plot of Hardcover Sales');

##################################
##### TUNNEL TRAFFIC EXAMPLE #####
##################################

simplefilter("ignore")  # ignore warnings to clean up output cells

# Set Matplotlib defaults
plt.style.use("seaborn-whitegrid")
plt.rc("figure", autolayout=True, figsize=(11, 4))
plt.rc(
    "axes",
    labelweight="bold",
    labelsize="large",
    titleweight="bold",
    titlesize=14,
    titlepad=10,
)
plot_params = dict(
    color="0.75",
    style=".-",
    markeredgecolor="0.25",
    markerfacecolor="0.25",
    legend=False,
)

tunnel = pd.read_csv("tunnel.csv", parse_dates=["Day"])
tunnel = tunnel.set_index("Day")
tunnel = tunnel.to_period()

df_tunnel = tunnel.copy()
df_tunnel['Time'] = np.arange(len(tunnel.index))

# Training data
X = df_tunnel.loc[:, ['Time']]  # features
y = df_tunnel.loc[:, 'NumVehicles']  # target

# Train the model
model = LinearRegression()
model.fit(X, y)

# Store the fitted values as a time series with the same time index as
# the training data
y_pred = pd.Series(model.predict(X), index=X.index)

ax1 = y.plot(**plot_params)
ax1 = y_pred.plot(ax=ax1, linewidth=3)
ax1.set_title('Time Plot of Tunnel Traffic');

df_tunnel['Lag_1'] = df_tunnel['NumVehicles'].shift(1)
# Need to decide what to do with missing values produced when creating lag features.
# In this case, we drop nan values

X = df_tunnel.loc[:, ['Lag_1']]
X.dropna(inplace=True) # drop missing values in the feature set
y = df_tunnel.loc[:, 'NumVehicles'] # create the target
y, X = y.align(X, join='inner') # drop corresponding values in target

model=LinearRegression()
model.fit(X, y)

y_pred = pd.Series(model.predict(X), index=X.index)

fig, ax = plt.subplots()
ax.plot(X['Lag_1'], y, '.', color='0.25')
ax.plot(X['Lag_1'], y_pred)
ax.set_aspect('equal')
ax.set_ylabel('NumVehicles')
ax.set_xlabel('Lag_1')
ax.set_title('Lag Plot of Tunnel Traffic');

fig, ax = plt.subplots()
ax = y.plot(**plot_params)
ax = y_pred.plot()