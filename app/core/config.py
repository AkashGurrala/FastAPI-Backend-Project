import os
from dotenv import load_dotenv

load_dotenv()


APP_ENV = os.getenv("APP_ENV", "dev")

DEV_DB_CONFIG = {
    "dbname": os.getenv("DEV_DB_NAME"),
    "user": os.getenv("DEV_DB_USER"),
    "password": os.getenv("DEV_DB_PASSWORD"),
    "host": os.getenv("DEV_DB_HOST"),
    "port": os.getenv("DEV_DB_PORT")
}

TEST_DB_CONFIG = {
    "dbname": os.getenv("TEST_DB_NAME"),
    "user": os.getenv("TEST_DB_USER"),
    "password": os.getenv("TEST_DB_PASSWORD"),
    "host": os.getenv("TEST_DB_HOST"),
    "port": os.getenv("TEST_DB_PORT")
}

# Choosing active configuration
if APP_ENV == "test":
    DB_CONFIG = TEST_DB_CONFIG
else:
    DB_CONFIG = DEV_DB_CONFIG
