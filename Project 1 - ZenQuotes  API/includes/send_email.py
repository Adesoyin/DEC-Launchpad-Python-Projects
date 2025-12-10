import smtplib #simple mail transfer protocol library
from email.mime.text import MIMEText #to send HTML email
from email.mime.multipart import MIMEMultipart #to send HTML email with multiple parts
import os
from dotenv import load_dotenv
from datetime import datetime
from includes.logging_info import logging_config

load_dotenv()
logging = logging_config()

SENDER_EMAIL = os.getenv("sender_email")
SENDER_PASSWORD = os.getenv("sender_password")
ADMIN_EMAIL = os.getenv("admin_email")  

def send_email(recipient, subject, body):
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html"))

    try:
        #with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=30) as server:
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        logging.info(f"Email sent successfully to {recipient}")
        return True
    except Exception as e:
        logging.error(f"Failed to send email to {recipient}: {e}")
        return False
    
def handle_failure_action():
    logging.info(f'Failed to send summary email to admin, timed out')

# Send admin the summary report
def send_summary_report(frequency, results, quote, author):
    """This sends summary email to the admin after every daily run"""
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

    <p><small>This is an automated report from the Zenquote project scheduler.</small></p>
    <p><small>Do not reply</small></p>
    """

    # Send the summary to admin
    if send_email(ADMIN_EMAIL, subject, body):
        send_email(ADMIN_EMAIL, subject, body)
        logging.info(f'Summary report sent to admin: {ADMIN_EMAIL}')
    else:
        handle_failure_action()
