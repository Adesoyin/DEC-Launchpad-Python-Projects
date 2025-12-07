from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from includes.logging_info import logging_config

logging = logging_config()
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


def get_engine():
    try:
        engine = create_engine(
            f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
        )
        logging.info("SQLAlchemy engine created successfully")
        return engine

    except Exception as e:
        logging.error(f"Failed to create SQLAlchemy engine: {e}")
        raise


if __name__ == "__main__":
    try:
        engine = get_engine()
        conn = engine.connect()
        print("Connection successful!")
        conn.close()
    except Exception as e:
        print(f"Connection failed: {e}")
