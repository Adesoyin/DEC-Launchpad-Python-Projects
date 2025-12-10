import datetime
from includes.logging_info import logging_config
from includes.dbconnection import get_engine
from collections import namedtuple

logging = logging_config()


User = namedtuple('User', ['email', 'firstname', 'frequency'])
                           
def get_users(frequency):
    try:
        engine = get_engine()
        conn = engine.raw_connection()
        cur=conn.cursor()
        query = """
            SELECT email_address, firstname, email_frequency_preference
            FROM dbo.users
            WHERE subscription_status = 'Active'
                AND email_frequency_preference = %s;
        """
        cur.execute(query, (frequency,))
        rows = cur.fetchall()
        users = [User(email=row[0], firstname=row[1], frequency=row[2])
                        for row in rows]
        logging.info(f"Retrieved {len(users)} active {frequency} user(s).")
        return users

    except Exception as e:
        logging.error(f"Database users query failed: {e}")
        return []
    finally:
        if conn:
            conn.close()
    