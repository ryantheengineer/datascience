# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 11:10:56 2023

@author: Ryan.Larson
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt


df = pd.read_csv("Daily activity metrics.csv")

df["Date"] = pd.to_datetime(df.Date, format='%m/%d/%Y')
df["7 Day Avg Steps"] = df["Step count"].rolling(7).mean()
df["30 Day Avg Steps"] = df["Step count"].rolling(30).mean()
df["90 Day Avg Steps"] = df["Step count"].rolling(90).mean()
# df["7 Day Avg Steps"] = df["Step count"].rolling(7).mean().shift(-3)
# df["30 Day Avg Steps"] = df["Step count"].rolling(30).mean().shift(-15)
# df["90 Day Avg Steps"] = df["Step count"].rolling(90).mean().shift(-45)
df_2022 = df[df["Date"].dt.year == 2022]
df_sep22 = df_2022[df_2022["Date"].dt.month == 9]
df_steps = df[["Date", "Step count", "7 Day Avg Steps", "30 Day Avg Steps", "90 Day Avg Steps"]]

# sns.scatterplot(data=df, x="Step count", y="Calories (kcal)")
plt.figure(dpi=300)
sns.scatterplot(data=df, x="Date", y="Step count", hue="Calories (kcal)", palette="GnBu")

plt.figure(dpi=300)
sns.scatterplot(data=df_2022, x="Date", y="Step count", hue="Calories (kcal)", palette="GnBu")
sns.lineplot(data=df_2022, x="Date", y="7 Day Avg Steps")
sns.lineplot(data=df_2022, x="Date", y="30 Day Avg Steps")

plt.figure(dpi=300)
# sns.scatterplot(data=df, x="Date", y="Step count", hue="Calories (kcal)", palette="GnBu")
sns.lineplot(data=df, x="Date", y="7 Day Avg Steps", label="7 Day Avg")
sns.lineplot(data=df, x="Date", y="30 Day Avg Steps", label="30 Day Avg")
sns.lineplot(data=df, x="Date", y="90 Day Avg Steps", label="90 Day Avg")


plt.figure(dpi=300)
sns.scatterplot(data=df, x="Step count", y="Calories (kcal)", palette="Blues")

plt.figure(dpi=300)
sns.scatterplot(data=df, x="Move Minutes count", y="Calories (kcal)", palette="Blues")
