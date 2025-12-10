from includes.logging_info import logging_config
from includes.dbconnection import get_engine
from psycopg2.extras import execute_values

logging=logging_config()

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