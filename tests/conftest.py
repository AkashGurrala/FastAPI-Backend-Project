import os

os.environ["APP_ENV"] = "test"

from app.db.connection import get_db_connection

def pytest_sessionstart(session):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE products RESTART IDENTITY CASCADE;")