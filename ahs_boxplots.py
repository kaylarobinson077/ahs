import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

raw_data["OMB13CBSA"] = raw_data["OMB13CBSA"].replace({
        "'12060'": 'Atlanta-Sandy Springs-Roswell, GA',
        "'12580'": 'Baltimore-Columbia-Towson, MD',
        "'13820'": 'Birmingham-Hoover, AL',
        "'14460'": 'Boston-Cambridge-Newton, MA-NH',
        "'16980'": 'Chicago-Naperville-Elgin, IL-IN-WI',
        "'17140'": 'Cincinnati, OH-KY-IN',
        "'17460'": 'Cleveland-Elyria, OH',
        "'19100'": 'Dallas-Fort Worth-Arlington, TX',
        "'19740'": 'Denver-Aurora-Lakewood, CO',
        "'19820'": 'Detroit-Warren-Dearborn, MI',
        "'26420'": 'Houston-The Woodlands-Sugar Land, TX',
        "'28140'": 'Kansas City, MO-KS',
        "'29820'": 'Las Vegas-Henderson-Paradise, NV',
        "'31080'": 'Los Angeles-Long Beach-Anaheim, CA',
        "'32820'": 'Memphis, TN-MS-AR',
        "'33100'": 'Miami-Fort Lauderdale-West Palm Beach, FL',
        "'33340'": 'Milwaukee-Waukesha-West Allis, WI',
        "'33460'": 'Minneapolis-St. Paul-Bloomington, MN-WI',
        "'35380'": 'New Orleans-Metairie, LA',
        "'35620'": 'New York-Newark-Jersey City, NY-NJ-PA',
        "'36420'": 'Oklahoma City, OK',
        "'37980'": 'Philadelphia-Camden-Wilmington, PA-NJ-DE-MD',
        "'38060'": 'Phoenix-Mesa-Scottsdale, AZ',
        "'38300'": 'Pittsburgh, PA',
        "'38900'": 'Portland-Vancouver-Hillsboro, OR-WA',
        "'39580'": 'Raleigh, NC',
        "'40060'": 'Richmond, VA',
        "'40140'": 'Riverside-San Bernardino-Ontario, CA',
        "'40380'": 'Rochester, NY',
        "'41700'": 'San Antonio-New Braunfels, TX',
        "'41860'": 'San Francisco-Oakland-Hayward, CA',
        "'41940'": 'San Jose-Sunnyvale-Santa Clara, CA',
        "'42660'": 'Seattle-Tacoma-Bellevue, WA',
        "'45300'": 'Tampa-St. Petersburg-Clearwater, FL',
        "'47900'": 'Washington-Arlington-Alexandria, DC-VA-MD-WV',
        "'99998'": 'All other metropolitan areas',
        "'99999'": 'Not in a metropolitan area'        
        })

raw_data = raw_data.assign(COMCOST_monthly = raw_data.COMCOST / 12)


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


#limit_toll = (raw_data['TOLL'] >= 0)
#df_filtered_toll = raw_data[limit_toll]

limit_com = raw_data['COMCOST'] >= 0
df_filtered_com = raw_data[limit_com]

my_order = df_filtered_com.groupby(by=["DIVISION"])["COMCOST"].median().sort_values(ascending = False).index

ax = sns.boxplot(y = "DIVISION", x = "COMCOST", data= df_filtered_com, palette="Pastel1", fliersize=0, order = my_order)
ax.set(xlabel = 'Commuting Cost (Annual)', ylabel = 'Census Division')
plt.xlim(-1000, 14000)

# lets look specifically at some metropolitan regions
# build a function to avoid repeated code
def boxplot_commute_region(region):
    df_region = df_filtered_com[df_filtered_com["DIVISION"] == region]
    my_order = df_region.groupby(by=["OMB13CBSA"])["COMCOST_monthly"].median().sort_values(ascending = False).index
    ax = sns.boxplot(y = "OMB13CBSA", x = "COMCOST_monthly", data= df_region, palette="Pastel1", fliersize=0, order = my_order)
    ax.set(xlabel = 'Commuting Cost (Annual)', ylabel = 'Metropolitan Region', title = region)
    plt.xlim(-1000, 17500)

# lets look specifically at some metropolitan regions

boxplot_commute_region('New England')
boxplot_commute_region('Middle Atlantic')
boxplot_commute_region('East North Central')
boxplot_commute_region('West North Central')
boxplot_commute_region('South Atlantic')
boxplot_commute_region('East South Central')
boxplot_commute_region('West South Central')
boxplot_commute_region('Mountain')
boxplot_commute_region('Pacific')
