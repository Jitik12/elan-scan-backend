import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()


def make_db():
    connection = psycopg2.connect(
        user=os.getenv("DB_USERNAME"),
        password=os.getenv("DB_PASSWORD"),
        host="localhost",
        port="5432",
        database=os.getenv("DB_NAME")
    )
    cursor = connection.cursor()
    return connection, cursor
