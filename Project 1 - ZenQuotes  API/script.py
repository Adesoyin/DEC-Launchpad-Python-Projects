#!/usr/bin/env python
import requests
import schedule
import time
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import psycopg2
from psycopg2.extras import execute_values
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv


# Logging Setup
# ----------------------------------------------------------
logging.basicConfig(
    filename="quotes_mailer.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# Load env, DB and credentials
# ----------------------------------------------------------
load_dotenv()
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
SENDER_EMAIL = os.getenv("sender_email")
SENDER_PASSWORD = os.getenv("sender_password")
ADMIN_EMAIL = os.getenv("admin_email")  



# Fetch Daily Quote (with Retry and Logging)
# ----------------------------------------------------------
def get_daily_quote(retries=2, delay=3):
    url = "https://zenquotes.io/api/today/"
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, timeout=15)
            #response.raise_for_status()
            data = response.json()
            quote = data[0]['q']
            author = data[0]['a']
            trans_date = datetime.now()
            logging.info(f"Fetched successfully: \"{quote}\" — {author}")
            return quote, author
        except Exception as e:
            logging.warning(f"Attempt {attempt} failed fetching quote: {e}")
            time.sleep(delay)
    logging.error("All retries failed fetching the quote.")
    return None, None

print(get_daily_quote())

# Writing Quote to Database
# ----------------------------------------------------------
def save_quote_to_db(quote, author):
    try:
        engine = create_engine(
            f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}' )
        # Prepare data
        current_date = datetime.now()
        zenquotes = pd.DataFrame(
            [{
                "quote": quote,
                "author": author,
                "trans_date": current_date
            }]
        )

        # Write to DB
        with engine.begin() as conn:
            zenquotes.to_sql("zenquote", conn, schema="dbo", if_exists="append", index=False)

        logging.info(f"Quote successfully inserted into zenquote table.")
        print("Quote successfully inserted into zenquote table.")

    except Exception as e:
        logging.error(f"Failed to insert quote into DB: {e}")
        print(f"Failed to insert quote into DB: {e}")

#Call the function to perform table insert
quote, author = get_daily_quote()
if quote:
    save_quote_to_db(quote, author)
else:
    logging.warning("No quote retrieved — skipping database insert.")


# Database Connection function
# ----------------------------------------------------------
def get_connection():
    return psycopg2.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
    )


# Retrieving Active Users Based on Frequency from the DB
# ----------------------------------------------------------
def get_users(frequency):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                query = """
                    SELECT email_address, firstname
                    FROM dbo.users
                    WHERE subscription_status = 'Active'
                      AND email_frequency_preference = %s;
                """
                cur.execute(query, (frequency,))
                users = cur.fetchall()
        logging.info(f"Retrieved {len(users)} active {frequency} user(s).")
        return users
    except Exception as e:
        logging.error(f"Database query failed: {e}")
        return []


# Send-Email Function
# ----------------------------------------------------------
def send_email(recipient, subject, body):
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        logging.info(f"Email sent successfully to {recipient}")
        return "Success"
    except Exception as e:
        logging.error(f"Failed to send email to {recipient}: {e}")
        return "Failed"


# Log Sent Email Results function
# ----------------------------------------------------------
def log_email_status(records):
    """
    records = list of tuples:
      (email_address, firstname, frequency, sent_status, quote, author, sent_at)
    """
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                insert_query = """
                    INSERT INTO email_log (
                        email_address, firstname, frequency,
                        sent_status, quote, author, sent_at
                    )
                    VALUES %s
                """
                execute_values(cur, insert_query, records)
                conn.commit()
        logging.info(f"Logged {len(records)} email results successfully.")
    except Exception as e:
        logging.error(f"Failed to insert email logs: {e}")


# Send me the summary report
# ----------------------------------------------------------
def send_summary_report(frequency, results, quote, author):
    total_sent = len(results)
    success_count = sum(1 for r in results if r[3] == "Success")
    failed_count = total_sent - success_count

    subject = f"Summary Report: {frequency} ZenQuotes — {datetime.now():%Y-%m-%d}"
    body = f"""
    <h3>{frequency} Quotes Summary Report</h3>
    <p><b>Date:</b> {datetime.now():%Y-%m-%d %H:%M:%S}</p>
    <p><b>Quote Sent:</b><br><em>"{quote}" — {author}</em></p>
    <p><b>Total Emails:</b> {total_sent}</p>
    <p><b>Successful:</b> {success_count}</p>
    <p><b>Failed:</b> {failed_count}</p>
    <hr>

    </b>This is an automated report from the Zenquote project scheduler.</p>
    <p>Do not reply</p>
    """

    # Send the summary to me
    send_email(ADMIN_EMAIL, subject, body)


# Main Function: Fetch Quote, Send Emails, Log Results, Report
# ----------------------------------------------------------
def send_quotes(frequency):
    quote, author = get_daily_quote()
    if not quote:
        logging.error("No quote retrieved; skipping email send.")
        return

    save_quote_to_db(quote, author)

    users = get_users(frequency)
    print(users)
    if not users:
        logging.warning("No users found; skipping email send.")
        return

    results = []
    for email, firstname in users:
        subject = f"Your {frequency} Quote ✨"
        body = f"""
        <html>
        <body style="font-family:Century Gothic, Arial, sans-serif; color:#333; font-size:14px;">
            <p>Dear {firstname},</p>
            <p style="font-style:italic; color:#555;">"{quote}"</p>
            <p style="margin-bottom:20px;">— {author}</p>
            
            <p>Have a great day!</p>

            <hr style="border: none; border-top: 1px solid #ccc; margin: 20px 0;">
            
            <p style="margin-top:10px;">Best regards,</p>
            <p><b>Zenquotes Hub</b></p>
            <p>For DEC Launchpad</p>
            </body>
        </html>
        """
        status = send_email(email, subject, body)
        results.append((email, firstname, frequency, status, quote, author, datetime.now()))

    # Log results and send mail to me
    log_email_status(results)
    send_summary_report(frequency, results, quote, author)
    logging.info(f"Completed {frequency} quote send cycle successfully.")

#Testing now if the script works up till this stage
#send_quotes("Daily")

# Scheduler Setup
# -----------------------------------------------------------
schedule.every().day.at("07:00").do(send_quotes, frequency="Daily")
schedule.every().saturday.at("07:00").do(send_quotes, frequency="Weekly")
logging.info("Scheduler started: Daily (7 AM), Weekly (Friday 7 AM)")



