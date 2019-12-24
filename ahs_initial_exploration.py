#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 16:54:49 2019

@author: krobinson2
"""

# import libraries
import pandas as pd
from scipy.stats import pearsonr


# exploration of american housing survey!

# read in the data

"""
Brainstorm : maybe build a model to predict housing value based on
a. just house info
b. just person info
and see if we can draw interesting conclusions by comparing predictiveness?

However, location w/in chicago is probably a massive confounding factor
Is there a way to deal with this? maybe a covariate to act as stand-in?
"""

# train test split
# encode categorical, continuous variables



fname = 'ahs2017n.csv'
#url = 'http://www2.census.gov/programs-surveys/ahs/2017/AHS%202017%20National%20PUF%20v3.0%20Flat%20CSV.zip?#'
raw_data = pd.read_csv(fname)
chicagoan = raw_data['OMB13CBSA'] == "'16980'"
chicago_data = raw_data[chicagoan]

#yvar = 'MORTAMT'
#yvar = 'RENT'
yvar = 'TOTHCAMT' # Monthly total housing costs

#xvar = 'PERPOVLVL' # Household income as percent of poverty threshold (rounded)
#xvar = 'HINCP' # Household Income (past 12 months)
#xvar = 'FS' # Flag indicating food stamp or supplemental nutrition assistance program recipency (past 12 months)
#xvar = 'RATINGHS' # Rating of unit as a place to live
#xvar = 'YRBUILT'
xvar = 'TOTROOMS'

corr, _ = pearsonr(chicago_data[xvar], chicago_data[yvar])
corr

# RENT - continuous
# TRANAMT - continuous, amount spent on commuting
# COMCOST - continuous, annual commuting cost
# COMDAYS - 0-7, days leave home for work
# COMTYPE - flag for type of transit used

