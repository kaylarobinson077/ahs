import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# data from: http://www2.census.gov/programs-surveys/ahs/2017/AHS%202017%20National%20PUF%20v3.0%20Flat%20CSV.zip?#
fname = 'Data/ahs2017n.csv'
raw_data = pd.read_csv(fname)

raw_data["TENURE"] = raw_data["TENURE"].replace({"'1'": 'Owned', "'2'": 'Rented', "'3'": 'Occupied without rent'})


incomes = raw_data["HINCP"]
incomes_positive = list(filter(lambda x: x >= 0, incomes))
incomes_5pp = np.percentile(incomes_positive, 5)
incomes_95pp = np.percentile(incomes_positive, 95)

# filter input df to only include these rows
limit_income = (raw_data['HINCP'] >= incomes_5pp) & (raw_data['HINCP'] < incomes_95pp)
df_filtered_income = raw_data[limit_income]

# add column for monthly income
df_filtered_income = df_filtered_income.assign(HINCP_monthly = df_filtered_income.HINCP / 12)

# filter to middle 90 % of housing costs to make the figure look nicer
hcost = raw_data["TOTHCAMT"]
hcost_positive = list(filter(lambda x: x >= 0, hcost))
hcost_5pp = np.percentile(hcost_positive, 5)
hcost_95pp = np.percentile(hcost_positive, 95)

limit_hcost = (df_filtered_income['TOTHCAMT'] >= hcost_5pp) & (df_filtered_income['TOTHCAMT'] < hcost_95pp)
df_filtered_hcost = df_filtered_income[limit_hcost]

# lets compare two continuous variables
limit_owners = df_filtered_hcost["TENURE"] == 'Owned'
df_owners = df_filtered_hcost[limit_owners]

limit_renters = df_filtered_hcost["TENURE"] == 'Rented'
df_renters = df_filtered_hcost[limit_renters]

# initialize color definitions
red = sns.color_palette("Reds")[-2]
blue = sns.color_palette("Blues")[-2]

# plot income vs. monthy housing costs
f, ax = plt.subplots(figsize=(8, 8))
ax = sns.kdeplot(df_owners["HINCP_monthly"], df_owners["TOTHCAMT"],
                 cmap="Reds", shade=True, shade_lowest=False)
ax = sns.kdeplot(df_renters["HINCP_monthly"], df_renters["TOTHCAMT"],
                 cmap="Blues", shade=True, shade_lowest=False)

# add regression lines
ax = sns.regplot(x="HINCP_monthly", y="TOTHCAMT", data=df_owners, color=red, scatter=False)
ax = sns.regplot(x="HINCP_monthly", y="TOTHCAMT", data=df_renters, color=blue, scatter=False)

ax.text(0, 3500, "Renters", size=16, color=blue)
ax.text(0, 3200, "Owners", size=16, color=red)
ax.set(xlabel = 'Household Income (Monthly)', ylabel = 'Total Housing Cost (Monthly)')


