# DEC-Launchpad-Python-Projects

This project tested my data engineering skills in building an automated quote email delivery platform using ZenQuotes API for MindFuel, a mental wellness startup. Get quotes from the API and automate daily sending to subscribers’ email. 

## Objectives
1. Pulls a new quote daily from ZenQuotes API - 
2. Personalizes and sends it to subscribed users via email at 7:00 AM
3. Logs activity and handles failures
4. Can scale to hundreds or thousands of users

## API Access and Quotes Ingestion
Python scripts was written to extract daily quotes from the ZenQuotes API site and ingested to a database with transaction date which signifies the date the quotes was extrxated. Check the [Quotes pulling script](Project\ 1\ -\ ZenQuotes\ \ API/quotespull.py) to view the code.

./quotespull.py can be run in terminal to view output while writing scripts.

## Data Ingestion into Database Table
A table was created on the postgres DB to host the daily quotes.
Lots of installtion was run in terminal to be able to pull the data.

## Users table 
A sample user table was created to host the user's email address, firstname and mail subscription (daily or weekly) which would prompt them. Check [the sql statement](Project\ 1\ -\ ZenQuotes\ \ API/SQLstatement.py)




pip install psycopg2-binary


