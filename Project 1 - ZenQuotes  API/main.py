import os, sys
from dotenv import load_dotenv
from datetime import datetime
from includes.logging_info import logging_config
from includes.get_daily_quote import get_daily_quote
from includes.save_quote_to_db import save_quote_to_db
from includes.get_users import get_users
from includes.send_email import send_email
from includes.send_email import send_summary_report
from includes.log_email import log_email_status

load_dotenv()
logging=logging_config()


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

    logging.info(f'Preparing to send mail to {len(users)} user(s)...')
    
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

    # Log results and send mail to admin
    log_email_status(results)
    send_summary_report(frequency, results, quote, author)
    logging.info(f"{frequency} quote process finished.")
    logging.info("=" * 50)
    logging.info( " " * 50)


def run_scheduler():
    """
    Main scheduler function - determines which frequency to run based on day.
    """
    try:
        # Weekly vs. daily logic
        today = datetime.now().strftime("%A")

        if today == "Saturday":
            logging.info(" " * 50)
            logging.info('Today is saturday-Running weekly quote')
            send_quotes("Weekly")
        else:
            logging.info(" " * 50)
            logging.info(f'Today is {today} - Running Daily quote')
            send_quotes("Daily")
        return "SUCCESS"
    except Exception as e:
        logging.info(f'Scheduler failed: {e}')
        return "FAILED"
    
if __name__ == "__main__":
    result=run_scheduler()
    sys.exit(0 if result == "SUCCESS" else 1)


