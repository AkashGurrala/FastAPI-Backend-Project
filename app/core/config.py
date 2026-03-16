import os


APP_ENV = os.getenv("APP_ENV", "dev")

DEV_DB_CONFIG = {
    "dbname": "fastapi_backend_db",
    "user": "fastapi_user",
    "password": "fastapi_user",
    "host": "localhost",
    "port": "5432"
}

TEST_DB_CONFIG = {
    "dbname": "fastapi_backend_db_test",
    "user": "fastapi_test_user",
    "password": "fastapi_test_user",
    "host": "localhost",
    "port": "5432"
}

# Choosing active configuration
if APP_ENV == "test":
    DB_CONFIG = TEST_DB_CONFIG
else:
    DB_CONFIG = DEV_DB_CONFIG
