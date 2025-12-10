import os
import requests
from dotenv import load_dotenv
from includes.logging_info import logging_config
from datetime import datetime
import time

load_dotenv()
logging = logging_config()

API_URL = os.getenv("API_URL")


# Fetch Daily Quote (with Retry and Logging)
def get_daily_quote(retries=2, delay=3):
    url = API_URL
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                logging.error(f'Error fetching quote: {response.status_code}')
                raise Exception({response.status_code})
            
            data = response.json()
            quote = data[0]['q']
            author = data[0]['a']
            trans_date = datetime.now()

            logging.info(f"Quote fetched successfully: \"{quote}\" — {author}")
            return quote, author
        except Exception as e:
            logging.warning(f"Attempt {attempt}/{retries} failed fetching quote: {e}")
            if (attempt < retries):
                time.sleep(delay)
    logging.error("All retries failed fetching the quote.")
    return None, None
