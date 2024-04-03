# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 13:15:26 2024

@author: Ryan.Larson
"""

import numpy as np
import pandas as pd
from scipy import stats

#%% Create empty dataframes to hold everything
colnames = ['66L', '66C', '66R',
            '54L', '54C', '54R',
            '42L', '42C', '42R',
            '30L', '30C', '30R',
            '18L', '18C', '18R',
            '6L', '6C', '6R']
dffrank = pd.DataFrame(columns=colnames)
dflow = pd.DataFrame(columns=colnames)

#%% Frankenstein Denali 6872 tank test data
frankdata = {'66L': [0.420,-0.300,0.300],
             '66C': [-0.180, 0.000, 0.000],
             '66R': [0.240, 0.420, -0.120],
             '54L': [0.900, 0.120, 0.600],
             '54C': [-0.060, -0.120, -0.120],
             '54R': [0.480, 0.600, 0.060],
             '42L': [0.660, 0.420, 0.900],
             '42C': [-0.180, -0.180, -0.240],
             '42R': [0.660, 0.780, 0.420],
             '30L': [1.140, 0.780, 1.140],
             '30C': [-0.240, -0.420, -0.300],
             '30R': [0.720, 1.020, 0.600],
             '18L': [1.800, 1.140, 1.380],
             '18C': [-0.300, -0.480, -0.300],
             '18R': [1.320, 1.560, 1.080],
             '6L': [1.680, 1.020, 1.560],
             '6C': [-0.300, -0.300, -0.240],
             '6R': [1.200, 1.560, 1.140]
             }

dffrank = pd.DataFrame(frankdata)

frank_means = []
frank_stds = []

for col in colnames:
    frank_means.append(np.mean(dffrank[col]))
    frank_stds.append(np.std(dffrank[col],ddof=1))

#%% Low-pressure Denali 6872 tank test data
lowdata = {'66L': [-0.240, -0.120, 0.060, -0.540],
           '66C': [-0.120, 0.000, 0.060, 0.120],
           '66R': [0.336, 0.360, 0.420, 0.480],
           '54L': [0.000, 0.120, -0.060, -0.060],
           '54C': [-0.060, -0.120, -0.060, -0.120],
           '54R': [0.660, -0.240, 0.900, 0.840],
           '42L': [0.540, 0.540, 0.360, -0.240],
           '42C': [-0.480 ,-0.060, -0.180, -0.120],
           '42R': [1.080, 1.380, 1.320, 1.500],
           '30L': [0.960, 1.020, 1.740, 0.720],
           '30C': [-0.360, -0.360, -0.360, -0.120],
           '30R': [1.620, 1.800, 1.740, 1.740],
           '18L': [1.020, 1.020, 0.900, 0.540],
           '18C': [-0.360, -0.300, -0.420, -0.120],
           '18R': [1.680, 1.980, 1.740, 1.860],
           '6L': [0.900, 0.900, 0.540, 0.120],
           '6C': [-0.120, 0.000, 0.000, 0.480],
           '6R': [1.362, 1.800, 1.320, 1.740]
           }

dflow = pd.DataFrame(lowdata)

low_means = []
low_stds = []

for col in colnames:
    low_means.append(np.mean(dflow[col]))
    low_stds.append(np.std(dflow[col],ddof=1))
    
#%% T-test comparisons of means
for col in colnames:
    varresult = stats.levene(dffrank[col], dflow[col])
    if varresult.pvalue > 0.05:
        equal_var=True
    else:
        equal_var=False
    result = stats.ttest_ind(dffrank[col], dflow[col], equal_var=equal_var)
    if result.pvalue > 0.05:
        print(f"{col}:\tNo statistical difference")
    else:
        print(f"{col}:\tStatistically significant difference found (p-val={result.pvalue})")