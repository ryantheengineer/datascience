# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 11:19:56 2023

@author: Ryan.Larson
"""
# %% Import Statements
import numpy as np
import pandas as pd
import datetime as dt
from datetime import timedelta, datetime

# %% Read in Data
filename = "C:/Users/Ryan.Larson.ROCKWELLINC/github/datascience/SalesOrdersByItemDetailandCustomerMJResults.xlsx"
df = pd.read_excel(filename)

# %% Organize
startdate = datetime(2022,5,1,0,0,0)
df_named = df[~df["Name"].isna()]
df_named = df_named[df_named["Date"]>startdate]
customers = df_named["Name"].unique()
reps = df_named["Sales Rep"].unique()

# Get dictionary with sales reps as keys and a list of their customers as the values
customers_by_rep = {rep:list(df_named[df_named["Sales Rep"]==rep]["Name"].unique()) for rep in reps}

reps_by_customer = {customer:list(df_named[df_named["Name"]==customer]["Sales Rep"].unique()) for customer in customers}

# %% Slice DataFrames
rep_avg_times = {}
for rep in reps:
    df_rep = df_named[df_named["Sales Rep"]==rep]
    # print(f"\nSales Rep:\t{rep}")
    customer_list = []
    mean_diffs = []
    diff_counts = []
    order_vals = []
    for customer in customers_by_rep[rep]:
        df_customer = df_rep[df_rep["Name"]==customer]
        df_customer_agg = df_customer.groupby(["Date"]).agg("sum")
        df_customer_date_productline = df_customer.groupby(["Date", "Income Account"]).agg("sum")
        avg_order_value = df_customer_agg["Amount"].sum()/len(df_customer_agg)
        # df_customer_agg["Avg Amount"] = df_customer_agg["Amount"]/df_customer_agg["Quantity"]
        # df_customer_agg = df_customer_agg.sort_values(by="Date", ascending=True)
        order_dates = df_customer.sort_values(by="Date",ascending=True)["Date"].unique()
        differences = np.diff(order_dates)/np.timedelta64(1,'D')        
        # differences = np.diff(df_customer.sort_values(by="Date",ascending=True)["Date"].unique())/np.timedelta64(1,'D')        
        diff_count = len(differences)
        median_difference = np.median(differences)
        std_difference = np.std(differences)
        mean_difference = np.mean(differences)
        # mean_difference = np.mean(np.diff(df_customer.sort_values(by="Date",ascending=True)["Date"].unique()))/np.timedelta64(1,'D')
        customer_list.append(customer)
        mean_diffs.append(mean_difference)
        diff_counts.append(diff_count)
        order_vals.append(avg_order_value)
    df_printout = pd.DataFrame({"Customer": customer_list,
                                "Avg Time Between Orders": mean_diffs,
                                "Difference Count": diff_counts,
                                "Avg Order Value": order_vals}
                               )
    rep_avg_times[rep] = df_printout

# %% Expected days until next order
for rep in reps:
    df_rep = rep_avg_times[rep]
    latest_orders = []
    expected_orders = []
    days_to_expected_order = []
    for customer in df_rep["Customer"]:
        avg_time = np.around(df_rep.loc[df_rep["Customer"]==customer, "Avg Time Between Orders"].item())
        df_customer = df_named[df_named["Name"]==customer]
        latest_order = df_customer["Date"].max().to_pydatetime()
        if np.isnan(avg_time):
            expected_next_order_date = np.nan
            days_to_expected = np.nan
        else:
            expected_next_order_date = latest_order + timedelta(days=avg_time)
            days_to_expected = pd.Timedelta(expected_next_order_date - datetime.today()).ceil("D")
        
        latest_orders.append(latest_order)
        expected_orders.append(expected_next_order_date)
        days_to_expected_order.append(days_to_expected)
        
    # Add ordering information as columns to rep_avg_times
    df_rep["Latest Order"] = latest_orders
    df_rep["Expected Next Ordering Date"] = expected_orders
    df_rep["Days Until Expected Order"] = days_to_expected_order
    
# %% Make filtered copy of rep_avg_times
# Remove any customers who have a difference count less than diff_threshold
diff_threshold = 5
rep_avg_times_filtered = {}
for rep in reps:
    df_rep = rep_avg_times[rep].copy()
    df_rep = df_rep[df_rep["Difference Count"]>=diff_threshold]
    rep_avg_times_filtered[rep] = df_rep
    
        