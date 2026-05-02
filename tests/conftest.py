import os
import psycopg2
import pytest
import requests

from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL")
PASSWORD = os.getenv("POSTGRES_PASSWORD")

TUTORIALS_BASE_URL = f"{API_URL}/tutorials"
USERS_BASE_URL = f"{API_URL}/users"

@pytest.fixture
def db_connect():
    # setup: DB connection
    conn = psycopg2.connect(
        dbname="django_rest",
        user="postgres",
        password=PASSWORD,
        host="127.0.0.1",
        port="5432"
    )
    cur = conn.cursor()

    # return cursor and connection objects
    yield {"cursor": cur, "connection": conn}

    # teardown: close cursor and connection
    cur.close()
    conn.close()

@pytest.fixture(autouse=True)
def prepare_system():
    requests.delete(TUTORIALS_BASE_URL)
    requests.delete(USERS_BASE_URL)
