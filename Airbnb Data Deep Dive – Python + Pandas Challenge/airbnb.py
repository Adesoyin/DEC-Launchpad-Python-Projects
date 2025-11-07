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
airbnb_data.to_csv('airbnb_listings_london.csv', index=False)
