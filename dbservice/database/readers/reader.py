import os
import psycopg2
import subprocess
from datetime import datetime,  timedelta

def open_connection():
    # remote version
    db_url = os.environ.get('DATABASE_URL')

    # local version
    if db_url is None or db_url == "sqlite:///db.sqlite3":
        proc = subprocess.Popen('heroku config:get DATABASE_URL -a rqa', stdout=subprocess.PIPE, shell=True)
        db_url = proc.stdout.read().decode('utf-8').strip() + '?sslmode=require'

    conn = psycopg2.connect(db_url)
    cur = conn.cursor()

    return cur, conn

def close_connection(cur, conn):
    cur.close()
    conn.close()

def db_reader(func):
    def wrapper(*args, **kwargs):
        cur, conn = open_connection()
        result = func(cur, *args, **kwargs)
        close_connection(cur, conn)
        return result
    return wrapper

@db_reader
def get_addresses(cur):
    print("Executing query: SELECT latitude, longitude FROM addresses;")
    cur.execute("SELECT address_id, latitude, longitude FROM addresses;")
    addresses = cur.fetchall()

    return addresses

@db_reader
def get_air_readings_for_address(cur, address_id, date_from, date_to, columns):
    print("Executing query: SELECT datetime, {0} FROM air_readings WHERE address_id = {1} AND datetime BETWEEN \'{2}\' AND \'{3}\' ORDER BY datetime ASC;".format(columns, address_id, date_from, date_to))
    cur.execute("SELECT datetime, {0} FROM air_readings WHERE address_id = {1} AND datetime BETWEEN \'{2}\' AND \'{3}\' ORDER BY datetime ASC;".format(columns, address_id, date_from, date_to))
    readings = cur.fetchall()

    return readings

@db_reader
def get_weather_readings_for_address(cur, address_id, date_from, date_to, columns):
    print("Executing query: SELECT datetime, {0} FROM weather_readings WHERE address_id = {1} AND datetime BETWEEN \'{2}\' AND \'{3}\' ORDER BY datetime ASC;".format(columns, address_id, date_from, date_to))
    cur.execute("SELECT datetime, {0} FROM weather_readings WHERE address_id = {1} AND datetime BETWEEN \'{2}\' AND \'{3}\' ORDER BY datetime ASC;".format(columns, address_id, date_from, date_to))
    readings = cur.fetchall()

    return readings