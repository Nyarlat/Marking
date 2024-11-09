import psycopg2
from .config import settings


def get_connection():
    conn = psycopg2.connect(
        dbname=settings.PG_DB,
        user=settings.PG_USER,
        password=settings.PG_PASSWORD,
        host=settings.PG_HOST,
        port=settings.PG_PORT
    )
    return conn
