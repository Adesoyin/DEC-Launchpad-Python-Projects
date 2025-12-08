import os, sys
from dotenv import load_dotenv
from datetime import datetime
from includes.logging_info import logging_config
from includes.get_daily_quote import get_daily_quote
from includes.save_quote_to_db import save_quote_to_db
from includes.get_users import get_users
from includes.send_email import send_email
from includes.dbconnection import get_engine
from psycopg2.extras import execute_values

load_dotenv()
logging=logging_config()

ADMIN_EMAIL = os.getenv("admin_email")
# Log Sent Email Results function
def log_email_status(records):
    """
    records = list of tuples:
      (email_address, firstname, frequency, sent_status, quote, author, sent_at)
    """
    try:
        engine = get_engine()
        conn = engine.raw_connection()
        #with get_connection() as conn:
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
        logging.info(f"Logged {len(records)} email results successfully into email_log table.")
    except Exception as e:
        logging.error(f"Failed to insert email logs: {e}")


# Send me the summary report
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

    <p><small>This is an automated report from the Zenquote project scheduler.</small></p>
    <p><small>Do not reply</small></p>
    """

    # Send the summary to admin
    send_email(ADMIN_EMAIL, subject, body)
    logging.info(f'Summary report sent to admin: {ADMIN_EMAIL}')


# Main Function: Fetch Quote, Send Emails, Log Results, Report
def send_quotes(frequency):
    logging.info(f'Starting {frequency} quote sending process....')

    quote, author = get_daily_quote()
    if not quote:
        logging.error("No quote retrieved; skipping email send.")
        return
    
    # Save quote to database
    save_quote_to_db(quote, author)

    # Get users
    users = get_users(frequency)
    print(users)
    if not users:
        logging.warning("No {frequency} users found; skipping email send.")
        return

    logging.info(f'Preparing to send emails to {len(users)} user(s)...')
    
    # Send emails
    results = []
    for user in users:
        subject = f"Your {frequency} Quote ✨"
        body = f"""
        <html>
        <body style="font-family:Century Gothic, Arial; color:#333; font-size:14px;">
            <p>Dear {user.firstname},</p>
            <p style="font-style:italic; color:#555;">"{quote}"</p>
            <p style="margin-bottom:20px;">— {author}</p>
            
            <p>Have a great day!</p>

            <hr style="border: none; border-top: 1px solid #ccc; margin: 20px 0;">
            
            <p style="margin-top:10px;">Best regards,</p>
            <p><b>Zenquotes Hub</b></p>
            <p><small>For DEC Launchpad</small></p>
            </body>
        </html>
        """
        status = send_email(user.email, subject, body)
        results.append((user.email, user.firstname, user.frequency, status, quote, author, datetime.now()))

    # Log results and send mail to me
    log_email_status(results)
    send_summary_report(frequency, results, quote, author)
    logging.info(f"Completed {frequency} quote send cycle successfully to admin.")
    logging.info("=" * 50)


def run_scheduler():
    """
    Main scheduler function - determines which frequency to run based on day.
    """
    try:
        # Weekly vs. daily logic
        today = datetime.now().strftime("%A")

        if today == "Saturday":
            logging.info('Today is saturday-Running weely quote')
            send_quotes("Weekly")
        else:
            logging.info(f'Today is {today} - Running Daily quote')
            send_quotes("Daily")
        return "SUCCESS"
    except Exception as e:
        logging.info(f'Scheduler failed: {e}')
        return "FAILED"
    
if __name__ == "__main__":
    result=run_scheduler()
    sys.exit(0 if result == "SUCCESS" else 1)


