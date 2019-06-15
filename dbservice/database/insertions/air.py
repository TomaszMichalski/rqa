# database.insertions.air.py
def insert_single_air_reading(cur, address_id, datetime, api, *args, **kwargs):
    pm1 = kwargs.get('pm1', None)
    pm10 = kwargs.get('pm10', None)
    pm25 = kwargs.get('pm25', None)

    print(
        "Executing query: INSERT INTO air_readings (datetime, weather, "
        "temperature, pressure, humidity, temp_min, temp_max, wind_speed, wind_degree, clouds, address_id, api_name) "
        "VALUES ({0}, {1}, {2}, {3},"
        " {4}, {5});".format(datetime, pm1, pm10, pm25, address_id , api))
    cur.execute(
        "INSERT INTO air_readings (datetime, pm1, pm10, pm25, address_id, api_name) "
        "VALUES (%s, %s, %s, %s, %s, %s);",
        (datetime, pm1, pm10, pm25, address_id, api))
