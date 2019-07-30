# worker.py
import os

import psycopg2
import subprocess
from database.insertions.misc import insert_nearest_airly_installations
from worker_functions import retrieve_and_insert_readings_for_all_addresses


def main():

    # remote version
    db_url = os.environ.get('DATABASE_URL')

    # local version
    if db_url is None:
        conn = psycopg2.connect(host='localhost', user='rqa_user', password='password', dbname='rqa_db')
    else:
        conn = psycopg2.connect(db_url)
    cur = conn.cursor()

    retrieve_and_insert_readings_for_all_addresses(cur)

    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
