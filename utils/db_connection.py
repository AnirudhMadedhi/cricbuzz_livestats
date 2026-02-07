import os
import sqlite3
from contextlib import contextmanager

DB_PATH = os.environ.get("CRICKET_DB_PATH", "cricket2.db")

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

@contextmanager
def db_cursor():
    conn = get_connection()
    try:
        yield conn.cursor()
        conn.commit()
    finally:
        conn.close()
