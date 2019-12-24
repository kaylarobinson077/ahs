#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 21:13:46 2019

@author: krobinson2
"""

import seaborn as sns
import pandas as pd
import numpy as np

# data from: http://www2.census.gov/programs-surveys/ahs/2017/AHS%202017%20National%20PUF%20v3.0%20Flat%20CSV.zip?#
fname = 'Data/ahs2017n.csv'
raw_data = pd.read_csv(fname)

raw_data["RODENT"] = raw_data["RODENT"].replace({"'1'": 'Daily', "'2'": 'Weekly', "'3'": 'Monthly', "'4'": 'A few times', "'5'": 'No signs'}) 
raw_data["TENURE"] = raw_data["TENURE"].replace({"'1'": 'Owned', "'2'": 'Rented', "'3'": 'Occupied without rent'})

# mutate fields of interest

# limit graphing to the middle 5%-95% of incomes, for simplicity
# omit missing value flags when calculating these
incomes = raw_data["HINCP"]
incomes_positive = list(filter(lambda x: x >0, incomes))
incomes_5pp = np.percentile(incomes_positive, 5)
incomes_95pp = np.percentile(incomes_positive, 95)

# filter input df to only include these rows
limit_income = (raw_data['HINCP'] >= incomes_5pp) & (raw_data['HINCP'] < incomes_95pp)
df_filtered_income = raw_data[limit_income]

# less wealthy people have more rodents
ax = sns.violinplot(y="HINCP", x="RODENT", data=df_filtered_income, palette="Pastel1", order = ['Daily', 'Weekly', 'Monthly', 'A few times', 'No signs'])
ax.set(xlabel = 'Rodent Sightings', ylabel = 'Household Income')


# why do owners make less than renters?
ax = sns.violinplot(y="HINCP", x="TENURE", data=df_filtered_income, palette="Pastel1", order = ['Owned', 'Rented'])
ax.set(xlabel = 'Household Ownership', ylabel = 'Household Income')


