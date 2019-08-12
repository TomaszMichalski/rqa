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
        proc = subprocess.Popen('heroku config:get DATABASE_URL -a rqa', stdout=subprocess.PIPE, shell=True)
        db_url = proc.stdout.read().decode('utf-8').strip() + '?sslmode=require'

    conn = psycopg2.connect(db_url)
    conn.autocommit = True
    cur = conn.cursor()

    retrieve_and_insert_readings_for_all_addresses(cur)

    # conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
