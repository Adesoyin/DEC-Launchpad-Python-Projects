import smtplib #simple mail transfer protocol library
from email.mime.text import MIMEText #to send HTML email
from email.mime.multipart import MIMEMultipart #to send HTML email with multiple parts
import os
from dotenv import load_dotenv
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
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=20) as server:
        #with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as server:
            #server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        logging.info(f"Email sent successfully to {recipient}")
        return "Success"
    except Exception as e:
        logging.error(f"Failed to send email to {recipient}: {e}")
        return "Failed"

#if __name__=="__main__":
#    send_email(*)