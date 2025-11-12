# JIRA Ticketing Automation
This repository contains an exploratory Jupyter notebook (`getrequestfield.ipynb`) used to inspect JIRA REST API field metadata and prepare payloads for automated issue creation/updating.

## Purpose
- Quickly discover and document JIRA field metadata required to construct valid issue creation payloads.
- Inspect allowed values/options for select-type fields and determine which fields are required for specific projects and issue types.
- Get daily request from customers from the database
- Creates a ticket for each customer on Jira automatically 

## Prerequisites
- Python 3.8+
- Libraries: requests, python-dotenv, 
- Access to a JIRA instance and an API token with appropriate permissions, and all authentication variables required from Jira

## Recommended environment variables
- JIRA_BASE_URL e.g. `https://your-domain.atlassian.net`
- JIRA_USER  (email/service account used in creating jira account)
- JIRA_TOKEN: API token
- REQUEST_ID: Gotten from the ticket creation link
- SERVICE_ID: Gotten from the ticket creation link


## Ticketing log

A table created to keep track of requests ticket has been raised for ad ensure multiple tickets are not created for the same request.

    CREATE TABLE integration_ticket_log (
        id SERIAL NOT NULL,
        name VARCHAR(255),
        issue_key VARCHAR(50),
        email VARCHAR(255) PRIMARY KEY,
        is_ticket_created VARCHAR(3) CHECK (is_ticket_created IN ('Yes', 'No')),
        is_form_updated VARCHAR(3) CHECK (is_form_updated IN ('Yes', 'No')),
        trans_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

It was ensured that before creating any ticket, the log table was checked ensuring no instance of that ticket in found using email address as primary key. This prevents deduplication of tickets.

## Notebook overview
- The notebook is commented properly and the output of each step can be checked in [the python file](getrequestfield.ipynb). 


 
