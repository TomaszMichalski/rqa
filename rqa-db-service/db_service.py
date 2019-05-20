# db_service.py
import os

import db_insertions
import psycopg2
import subprocess


def main():

    # remote version
    db_url = os.environ.get('DATABASE_URL')

    # local version
    if db_url is None:
        proc = subprocess.Popen('heroku config:get DATABASE_URL -a rqa', stdout=subprocess.PIPE, shell=True)
        db_url = proc.stdout.read().decode('utf-8').strip() + '?sslmode=require'

    conn = psycopg2.connect(db_url)
    cur = conn.cursor()

    #db_insert.insert_weather_for_all_points(cur)
    #db_insert.insert_air_for_all_installations(cur)
    conn.commit()

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
