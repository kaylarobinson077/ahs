import seaborn as sns
import pandas as pd
import numpy as np

# data from: http://www2.census.gov/programs-surveys/ahs/2017/AHS%202017%20National%20PUF%20v3.0%20Flat%20CSV.zip?#
fname = 'Data/ahs2017n.csv'
raw_data = pd.read_csv(fname)

# give readable names for division
raw_data["DIVISION"] = raw_data["DIVISION"].replace({
        "'1'": 'New England',
        "'2'": 'Middle Atlantic',
        "'3'": 'East North Central',
        "'4'": 'West North Central',
        "'5'": 'South Atlantic',
        "'6'": 'East South Central',
        "'7'": 'West South Central',
        "'8'": 'Mountain',
        "'9'": 'Pacific'})

hcost = raw_data["TOTHCAMT"]
hcost_positive = list(filter(lambda x: x >= 0, hcost))
hcost_5pp = np.percentile(hcost_positive, 5)
hcost_95pp = np.percentile(hcost_positive, 95)

limit_hcost = (raw_data['TOTHCAMT'] >= hcost_5pp) & (raw_data['TOTHCAMT'] < hcost_95pp)
df_filtered_hcost = raw_data[limit_hcost]

# order by median
my_order = df_filtered_hcost.groupby(by=["DIVISION"])["TOTHCAMT"].median().sort_values(ascending = False).index

# look at housing prices by census region
ax = sns.boxplot(y = "DIVISION", x = "TOTHCAMT", data= df_filtered_hcost, palette="Pastel1", order = my_order, fliersize=0)
ax.set(xlabel = 'Total Housing Cost (Monthly)', ylabel = 'Census Division')
