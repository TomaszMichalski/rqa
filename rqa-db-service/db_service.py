# db_service.py
import os

import airly_reader
import db_get
import db_insert
import psycopg2
import subprocess


def main():
    """   TODO: add getting data from APIs and sending them to database """

    # local version
    proc = subprocess.Popen('heroku config:get DATABASE_URL -a rqa', stdout=subprocess.PIPE, shell=True)
    db_url = proc.stdout.read().decode('utf-8').strip() + '?sslmode=require'

    # remote version
    # db_url = os.environ['DATABASE_URL']

    conn = psycopg2.connect(db_url)
    cur = conn.cursor()

    db_insert.insert_weather_for_all_points(cur)
    db_insert.insert_air_for_all_installations(cur)
    conn.commit()

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
