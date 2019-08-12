# database.insertions.air.py

import psycopg2


def insert_single_air_reading(cur, address_id, datetime, api, *args, **kwargs):
    pm1 = kwargs.get('pm1', None)
    pm10 = kwargs.get('pm10', None)
    pm25 = kwargs.get('pm25', None)

    cur.execute("SELECT * FROM weather_readings")
    print("Before insertion in air_readings: ")
    print(cur.rowcount)

    done = False

    for attempts in range(1000):
        if done:
            break
        try:
            cur.execute(
                "INSERT INTO air_readings (datetime, pm1, pm10, pm25, address_id, api_name) "
                "VALUES (%s, %s, %s, %s, %s, %s);",
                (datetime, pm1, pm10, pm25, address_id, api))
            done = True
        except psycopg2.Error as e:
            print("PostgreSQL Error {0}: {1}".format(e.args[0], e.args[1]))

    if done:
        print(
            "Executed query: INSERT INTO air_readings (datetime, weather, "
            "temperature, pressure, humidity, temp_min, temp_max, wind_speed, wind_degree, clouds, address_id, api_name) "
            "VALUES ({0}, {1}, {2}, {3},"
            " {4}, {5});".format(datetime, pm1, pm10, pm25, address_id, api))

    cur.execute("SELECT * FROM weather_readings")
    print("After insertion in weather_readings: ")
    print(cur.rowcount)
