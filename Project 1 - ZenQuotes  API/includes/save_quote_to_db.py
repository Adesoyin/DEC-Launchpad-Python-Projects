#import pandas as pd
from datetime import datetime
from includes.dbconnection import get_engine
from includes.get_daily_quote import get_daily_quote
from includes.logging_info import logging_config

logging = logging_config()

# Writing Quote to Database
def save_quote_to_db(quote, author):
    try:
        current_date = datetime.now()
        engine = get_engine()
        conn = engine.raw_connection()
        #with get_connection() as conn:
        with conn.cursor() as cur:
                # Prepare data
            insert_query = """
                INSERT INTO dbo.zenquote (quote, author, trans_date)
                VALUES (%s, %s, %s)
            """
            cur.execute(insert_query, (quote, author, current_date))
            conn.commit()

        logging.info(f"Quote successfully inserted into zenquote table.")
        print("Quote successfully inserted into zenquote table.")
        conn.commit()

    except Exception as e:
        logging.error(f"Failed to insert quote into DB: {e}")
        return False