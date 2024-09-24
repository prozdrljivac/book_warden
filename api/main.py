import sqlite3

from fastapi import FastAPI

from apps.routes import api_v1_router

app = FastAPI()

db_connection = sqlite3.connect("db/dev.db")

db_cursor = db_connection.cursor()
db_cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS books(
        id INTEGER PRIMARY KEY,
        title TEXT,
        description TEXT,
        author TEXT
    );
    """
)

# Query the system table to check if the "books" table exists
db_cursor.execute(
    """
    SELECT name FROM sqlite_master WHERE type='table' AND name='books';
    """
)

# Fetch the result
table_exists = db_cursor.fetchone()

db_cursor.close()
db_connection.close()

if table_exists:
    print("Books table successfully created.")

app.include_router(api_v1_router)
