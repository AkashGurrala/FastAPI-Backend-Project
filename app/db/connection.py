import psycopg2
from app.core.config import DB_CONFIG

def get_db_connection():
    connection = psycopg2.connect(**DB_CONFIG)
    return connection

def test_db_connection():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        #Safe test query
        cursor.execute("SELECT 1;")
        result = cursor.fetchone()

        print("Database connection successful:", result)

        cursor.close()
        conn.close()

    except Exception as e:
        print("Database connection failed", str(e))