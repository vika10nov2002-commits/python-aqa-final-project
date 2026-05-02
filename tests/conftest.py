import dotenv
import psycopg2
import pytest
import requests

TUTORIALS_BASE_URL = "http://127.0.0.1:8080/api/tutorials"
USERS_BASE_URL = "http://127.0.0.1:8080/api/users"

@pytest.fixture
def db_connect():
    # setup: DB connection
    conn = psycopg2.connect(
        dbname="django_rest",
        user="postgres",
        password=dotenv.get_key(".env","POSTGRES_PASSWORD"),
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
