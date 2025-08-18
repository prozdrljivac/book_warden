import sqlite3
from typing import Optional
from contextlib import contextmanager

from config.settings import get_settings

app_settings = get_settings()

@contextmanager
def db_transaction(connection_string: Optional[str] = None):
    connection = sqlite3.connect(connection_string or app_settings.db_url)
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()

def init_db():
    with db_transaction() as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS books(
                id INTEGER PRIMARY KEY,
                title TEXT,
                description TEXT,
                author TEXT
            );
            """
        )
