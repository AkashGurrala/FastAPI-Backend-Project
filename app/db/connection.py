import psycopg2

#DB Configurarion
DB_CONFIG = {
    "dbname": "fastapi_backend_db",
    "user": "fastapi_user",
    "password": "password",
    "host":"localhost",
    "port": "5432"
}

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

        # Always close cursor and connection
        cursor.close()
        conn.close()

    except Exception as e:
        print("Database connection failed", str(e))