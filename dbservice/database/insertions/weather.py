# database.insertions.weather.py
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

    print(
        "Executing query: INSERT INTO weather_readings (datetime, weather, "
        "temperature, pressure, humidity, temp_min, temp_max, wind_speed, wind_degree, clouds, address_id, api_name) "
        "VALUES ({0}, {1}, {2}, {3},"
        " {4}, {5}, {6}, {7}, {8}, {9},"
        " {10}, {11});".format(datetime, weather, temperature, pressure, humidity, temp_min, temp_max, wind_speed,
                               wind_degree, clouds, address_id, api))
    cur.execute(
        "INSERT INTO weather_readings (datetime, weather, "
        "temperature, pressure, humidity, temp_min, temp_max, wind_speed, wind_degree, clouds, address_id, api_name) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",
        (datetime, weather, temperature, pressure, humidity, temp_min, temp_max,
         wind_speed, wind_degree, clouds, address_id, api))
