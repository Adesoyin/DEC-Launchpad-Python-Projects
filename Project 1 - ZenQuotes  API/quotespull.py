#!/usr/bin/env python
#Import necessary libraries
import requests
import pandas as pd
from datetime import datetime
import time as t
import random as r
import json # Convert data to JSON format
#import fake

# Url to pull daily quotes from ZenQuotes API
url = "https://zenquotes.io/api/today/"

# Pull data from the API
get = requests.get(url)

data = get.json()
quote = data[0]['q']
author = data[0]['a']
currentdate = datetime.now()

print (quote)
print (author)
print (currentdate)

# create a dataframe to hold the data

data ={"quote": quote,
                "author": author,
                "trans_date": currentdate
}
zenquotes = pd.DataFrame([data])

print(zenquotes)

# connect to the database
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
load_dotenv()
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
conn = engine.connect()

#write data to the database table
zenquotes.to_sql('zenquote', conn, if_exists='append', index=False)
conn.close()
print("Data inserted successfully into zenquote table")



