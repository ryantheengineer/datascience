# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 09:37:59 2023

@author: Ryan.Larson
"""

import numpy as np
import pandas as pd
import datetime as dt
from datetime import timedelta, datetime, date
import calendar

def get_past_n_months(current_month, current_year, n):
    months = []
    for _ in range(n):
        if current_month == 1:  # If current month is January, decrement year and set month to December
            current_month = 12
            current_year -= 1
        else:
            current_month -= 1

        months.append((current_month, current_year))
        
    months.reverse()

    return months

# Step 1: Read the original data into a DataFrame
# filename = "C:/Users/Ryan.Larson.ROCKWELLINC/Downloads/SalesOrdersByItemDetailandCustomerMJResults.xlsx"
filename = "C:/Users/Ryan.Larson.ROCKWELLINC/github/datascience/SalesOrdersByItemDetailandCustomerMJResults.xlsx"
data = pd.read_excel(filename)  # Replace 'your_csv_file.csv' with the actual filename or path
startdate = datetime(2023,2,1,0,0,0)
data = data[~data["Name"].isna()]
data = data[~data["Income Account"].isna()]
data = data[~data["Product Line"].isna()]
data = data[~data["Sales Rep"].isna()]
data = data[data["Date"]>startdate]
data = data.reset_index(drop=True)

# Step 2: Add a column called "Latest Order" showing the maximum Date value for each combination of Sales Rep, Name, and Product Line
data['Date'] = pd.to_datetime(data['Date'])  # Convert 'Date' column to datetime type
latest_order_dates = data.groupby(['Sales Rep', 'Name', 'Product Line'])['Date'].max()
data['Latest Order'] = data.apply(lambda row: latest_order_dates[row['Sales Rep'], row['Name'], row['Product Line']], axis=1)

# Step 3: Calculate the average number of days between Date values for each Sales Rep, Name, and Product Line combination
# data['Avg Time Between Orders'] = data.groupby(['Sales Rep', 'Name', 'Product Line'])['Date'].transform(lambda x: x.diff().mean())
data['Avg Time Between Orders'] = np.abs(data.groupby(['Sales Rep', 'Name', 'Product Line'])['Date'].transform(lambda x: x.diff().mean().days))

# Step 4: Using the Python library datetime, add a co lumn called "Expected Next Order"
data['Expected Next Order'] = data['Latest Order'] + data['Avg Time Between Orders'].apply(pd.to_timedelta,unit = 'D')

# Step 5: Add another column called "Days Until Expected Order" by taking the difference between the "Expected Next Order" column and the current date
current_date = datetime.combine(date.today(), datetime.min.time())
# data['Days Until Expected Order'] = (data['Expected Next Order'] - current_date).dt.days

# Step 6: Use Pandas multi-indexing to separate the data out by the index levels: Sales Rep, Name, and Product Line
multi_index_cols = ['Sales Rep', 'Name', 'Product Line']
multi_indexed_data = data.set_index(multi_index_cols)

# Optionally, sort the multi-index if needed
multi_indexed_data.sort_index(inplace=True)

# Get the list of unique labels (Sales Rep, Name, Product Line)
unique_labels = list(multi_indexed_data.index.unique())

# Iterate through the unique labels and get the corresponding slices

today = dt.date.today()
month = today.month
year = today.year
n_months = 12    # Do not use a value greater than 12 or it will cause label problems
past_months = get_past_n_months(month, year, n_months)
past_months_abbr = [calendar.month_abbr[m[0]] for m in past_months]
months = get_past_n_months(month+1,year,12)
# months = get_past_n_months(3,2024,12)
months_abbr = [calendar.month_abbr[m[0]] for m in months]
years_short = [m[1]-2000 for m in months]

month_year_abbr = [m+f" {years_short[i]}" for i,m in enumerate(months_abbr)]


cols = [m for m in month_year_abbr]
# cols = [m for m in months_abbr]
other_labels = ['Median Amount',
                'Latest Order',
                'Avg Days Between Orders',
                'Expected Next Order']
# other_labels = ['Sale Days',
#                 'Median Amount',
#                 'Latest Order',
#                 'Avg Days Between Orders',
#                 'Expected Next Order',
#                 'Days Until Expected Order']
cols.extend(other_labels)

ind = pd.MultiIndex.from_tuples([], names=('Sales Rep', 'Name', 'Product Line'))
df = pd.DataFrame(columns=cols, index=ind)

for i,label in enumerate(unique_labels):
    label_slice = multi_indexed_data.loc[label]
    
    # Get information on amounts for each of the last six months
    total_spent = []
    # for m in past_months:
    for m in months:
        mask = ((label_slice['Date'].dt.month==m[0]) & (label_slice['Date'].dt.year==m[1]))
        total_spent.append(label_slice.loc[mask]['Amount'].sum())
        
    nobs = len(label_slice)
    avg_amount = label_slice['Amount'].median()
    latest_order = label_slice['Latest Order'].iloc[0]
    avg_days_between = label_slice['Avg Time Between Orders'].iloc[0]
    next_expected = label_slice['Expected Next Order'].iloc[0]
    # days_until_expected = label_slice['Days Until Expected Order'].iloc[0]
    
    df.loc[label, :] = [total_spent[0],
                        total_spent[1],
                        total_spent[2],
                        total_spent[3],
                        total_spent[4],
                        total_spent[5],
                        total_spent[6],
                        total_spent[7],
                        total_spent[8],
                        total_spent[9],
                        total_spent[10],
                        total_spent[11],
                        avg_amount,
                        latest_order,
                        avg_days_between,
                        next_expected]
    # df.loc[label, :] = [total_spent[0],
    #                     total_spent[1],
    #                     total_spent[2],
    #                     total_spent[3],
    #                     total_spent[4],
    #                     total_spent[5],
    #                     total_spent[6],
    #                     total_spent[7],
    #                     total_spent[8],
    #                     total_spent[9],
    #                     total_spent[10],
    #                     total_spent[11],
    #                     nobs,
    #                     avg_amount,
    #                     latest_order,
    #                     avg_days_between,
    #                     next_expected,
    #                     days_until_expected]
    
# Convert columns to the correct data types
# for m in past_months_abbr:
for m in month_year_abbr:
# for m in months_abbr:
    df[m] = df[m].astype(float)
# df['Sale Days'] = df['Sale Days'].astype(float)
df['Median Amount'] = df['Median Amount'].astype(float)
df['Latest Order'] = pd.to_datetime(df['Latest Order'])
df['Avg Days Between Orders'] = df['Avg Days Between Orders'].astype(float)
df['Expected Next Order'] = pd.to_datetime(df['Expected Next Order'])
# df['Days Until Expected Order'] = df['Days Until Expected Order'].astype(float)

reps = df.index.unique(level='Sales Rep')
customers = df.index.unique(level='Name')

data_by_rep = {rep:df.loc[pd.IndexSlice[rep,:,:],:] for rep in reps}

# Edit column order to match Vaughn's preference
for key, df in data_by_rep.items():
    last_three_columns = df.columns[-3:]
    other_columns = df.columns[:-3]
    new_order = list(last_three_columns) + list(other_columns)
    data_by_rep[key] = df[new_order]
    
# Turn all zeros in all dataframes to nan
for key, df in data_by_rep.items():
    df.replace(0, np.nan, inplace=True)
