# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 09:37:59 2023

@author: Ryan.Larson
"""

import pandas as pd

# Sample data with multiple entries for the same customer on the same date
data = {
    'Customer': ['CustomerA', 'CustomerA', 'CustomerA', 'CustomerB', 'CustomerB'],
    'Date': ['2023-08-01', '2023-08-01', '2023-08-02', '2023-08-01', '2023-08-03'],
    'Income Account': ['AccountX', 'AccountY', 'AccountX', 'AccountX', 'AccountY'],
    'Quantity': [10, 15, 20, 5, 8],
    'Amount': [100, 150, 200, 50, 80]
}

df = pd.DataFrame(data)

# Convert 'Date' column to datetime type
df['Date'] = pd.to_datetime(df['Date'])

# Group by 'Customer', 'Date', and 'Income Account' and calculate average Quantity and Amount
grouped_df = df.groupby(['Customer', 'Date', 'Income Account']).agg({
    'Quantity': 'mean',
    'Amount': 'mean'
}).reset_index()

# Group by 'Customer' and 'Income Account' and calculate average Quantity and Amount over all Dates
result_df = grouped_df.groupby(['Customer', 'Income Account']).agg({
    'Quantity': 'mean',
    'Amount': 'mean'
}).reset_index()

print(result_df)
