#!/usr/bin/env python
#AIR BNB DATA DEEP DIVE - PYTHON + PANDAS CHALLENGE

#==========================================
# Importing libraries
import pandas as pd
import numpy as np
import requests
import datetime as dt


#==========================================
#Loading the dataset
url = 'https://data.insideairbnb.com/united-kingdom/england/london/2025-06-10/data/listings.csv'

#Reading the dataset
airbnb_data = pd.read_csv(url)
airbnb_data.head()
#Loading the dataset to a csv file if it exist, replaces the old one
airbnb_data.to_csv('airbnb_listings_london.csv', index=False,header=True)

#==========================================
# Dislaying the basic information about the dataset
# Data information
airbnb_data.info()
# Statistical summary
airbnb_data.describe()
# Display top 5 rows to see how structured the data is
airbnb_data.head()
# Checking for missing values in the dataset
missing_data = airbnb_data.isnull().sum()
print

#==========================================



#Check for missing values, duplicated rows, and unusual data types.