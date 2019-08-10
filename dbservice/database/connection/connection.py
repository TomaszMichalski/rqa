# connection.py
import os
import psycopg2


def open_database_connection():
    db_url = os.environ.get('DATABASE_URL')

    if db_url is None:
        # local version
        conn = psycopg2.connect(host='localhost', user='rqa_user', password='password', dbname='rqa_db')
    else:
        # remote version
        conn = psycopg2.connect(db_url)
    cur = conn.cursor()

    return cur, conn
