# database.insertions.weather.py

import psycopg2


def insert_single_weather_reading(cur, address_id, datetime, api, *args, **kwargs):
    weather = kwargs.get('weather', None)
    temperature = kwargs.get('temperature', None)
    pressure = kwargs.get('pressure', None)
    humidity = kwargs.get('humidity', None)
    temp_min = kwargs.get('temp_min', None)
    temp_max = kwargs.get('temp_max', None)
    wind_speed = kwargs.get('wind_speed', None)
    wind_degree = kwargs.get('wind_degree', None)
    clouds = kwargs.get('clouds', None)

    cur.execute("SELECT * FROM weather_readings")
    print("Before insertion in weather_readings: ")
    print(cur.rowcount)

    done = False

    for attempts in range(3000):
        if done:
            break
        try:
            cur.execute(
                "INSERT INTO weather_readings (datetime, weather, "
                "temperature, pressure, humidity, temp_min, temp_max, wind_speed, wind_degree, clouds, address_id, api_name) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",
                (datetime, weather, temperature, pressure, humidity, temp_min, temp_max,
                 wind_speed, wind_degree, clouds, address_id, api))
            done = True
        except psycopg2.Error as e:
            print("PostgreSQL Error {0}".format(e))

    if done:
        print(
            "Executed query: INSERT INTO weather_readings (datetime, weather, "
            "temperature, pressure, humidity, temp_min, temp_max, wind_speed, wind_degree, clouds, address_id, api_name) "
            "VALUES ({0}, {1}, {2}, {3},"
            " {4}, {5}, {6}, {7}, {8}, {9},"
            " {10}, {11});".format(datetime, weather, temperature, pressure, humidity, temp_min, temp_max, wind_speed,
                                   wind_degree, clouds, address_id, api))

    cur.execute("SELECT * FROM weather_readings")
    print("After insertion in weather_readings: ")
    print(cur.rowcount)
