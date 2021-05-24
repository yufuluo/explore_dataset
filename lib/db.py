import sqlite3
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

DB_PATH = './db/database.db'

def get_db_connection():
    """Connect to SQLite database.

    Args:
        db_path: A string. The path to a db file.

    Returns:
        A Connection object that represents the database.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
    except Exception as e:
        logging.error('Error', exc_info=True)
    conn.row_factory = sqlite3.Row
    return conn
