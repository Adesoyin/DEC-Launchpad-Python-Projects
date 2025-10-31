# DEC-Launchpad-Python-Projects

This project tested my data engineering skills in building an automated quote email delivery platform using ZenQuotes API for MindFuel, a mental wellness startup. Get quotes from the API and automate daily sending to subscribers’ email. 

## Objectives
1. Pulls a new quote daily from ZenQuotes API - https://zenquotes.io/api/today/
2. Personalizes and sends it to subscribed users via email at 7:00 AM
3. Logs activity and handles failures
4. Can scale to hundreds or thousands of users

## API Access and Quotes Ingestion
Python scripts was written to extract daily quotes from the ZenQuotes API site and ingested to a database with transaction date which signifies the date the quotes was extrxated. Check the [.pyscript](script.py) to view the code.

./quotespull.py can be run in terminal to view output while writing scripts.

## Data Ingestion into Database Table
A table was created on the postgres DB to host the daily quotes.
Lots of installtion was run in terminal to be able to pull the data.

## Users table & Email delivery
A sample user table was created to host the user's email address, firstname and mail subscription (daily or weekly) which would prompt them. Check [the sql statement](SQLstatement.py)

Daily quotes were sent to the users that subscribed to the daily subscription and same for weekly subscription at 7:00AM. 

## Logging & Monitoring
Used execute_values() to bulk insert all email send results into email_log table by recording email address, firstname, frequency, quote, author, sent status, and timestamp. This would give a full send history for monitoring and analytics. Navigate to [quotes_mailer,log](quotes_mailer.log) to see log history.

Likewise, daily email stats and summary logs was sent to the admin tonote how many successful and failed emails.

A screenshot of email_log data

![alt text](images/email_log.png)

## Summary of Script Flow
Start
│
├─ Load environment vars and logging
├─ Fetch daily quote
├─ Save quote to DB
├─ Retrieve user list
├─ Send email to each user
├─ Log sent status in DB
└─ Schedule tasks daily/weekly



