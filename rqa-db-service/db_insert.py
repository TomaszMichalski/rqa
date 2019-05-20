import airly_reader
import db_get
import owm_reader
from datetime import datetime


def insert_point(cur, latitude, longitude):
    point_id = db_get.get_point_id_by_coord(cur, latitude, longitude)

    if point_id is None:
        print(
            "Executing query: INSERT INTO point (latitude, longitude) VALUES (%s, %s);".format(latitude, longitude))
        cur.execute("INSERT INTO point (latitude, longitude) VALUES (%s, %s);", (latitude, longitude))

    return db_get.get_point_id_by_coord(cur, latitude, longitude)


def insert_weather_for_all_points(cur):
    points = db_get.get_points(cur)
    for point in points:
        insert_weather_for_coord(cur, point[1], point[2])


def insert_weather_for_coord(cur, latitude, longitude):
    point_id = insert_point(cur, latitude, longitude)

    conditions = owm_reader.get_conditions(latitude, longitude)

    weather_info = conditions.get('weather')
    weather = ""
    for info in weather_info:
        weather += info.get('description') + '/'
    weather = weather[0:-1]

    dt = datetime.fromtimestamp(conditions.get('dt'))

    main_info = conditions.get('main')
    temperature = main_info.get('temp')
    pressure = main_info.get('pressure')
    humidity = main_info.get('humidity')
    temp_min = main_info.get('temp_min')
    temp_max = main_info.get('temp_max')

    wind_info = conditions.get('wind')
    wind_speed = wind_info.get('speed')
    wind_degree = wind_info.get('deg')

    cloud_info = conditions.get('clouds')
    clouds = cloud_info.get('all')

    print(
        "Executing query: INSERT INTO weather (point_id, datetime, weather, "
        "temperature, pressure, humidity, temp_min, temp_max, wind_speed, wind_degree, clouds) "
        "VALUES ({0}, {1}, {2}, {3},"
        " {4}, {5}, {6}, {7}, {8}, {9},"
        " {10});".format(point_id, datetime, weather, temperature, pressure, humidity, temp_min, temp_max, wind_speed,
                         wind_degree, clouds))
    cur.execute(
        "INSERT INTO weather (point_id, datetime, weather, "
        "temperature, pressure, humidity, temp_min, temp_max, wind_speed, wind_degree, clouds) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",
        (point_id, dt, weather, temperature, pressure, humidity, temp_min, temp_max, wind_speed, wind_degree, clouds))


def insert_air_for_all_installations(cur):
    installation_ids = db_get.get_installation_ids(cur)
    for iid in installation_ids:
        insert_air_for_id(cur, iid[0])


def insert_air_for_id(cur, iid):
    air_data = airly_reader.get_measurements(iid)
    if air_data is not None:
        current = air_data.get('current')
        raw_dt = current.get('tillDateTime')
        dt = raw_dt[0:10] + ' ' + raw_dt[11:19]
        pm1 = pm10 = pm25 = pressure = humidity = temperature = None
        values = current.get('values')
        for value in values:
            if value.get('name').lower() == "pm1":
                pm1 = value.get('value', None)
            if value.get('name').lower() == "pm10":
                pm10 = value.get('value', None)
            if value.get('name').lower() == "pm25":
                pm25 = value.get('value', None)
            if value.get('name').lower() == "pressure":
                pressure = value.get('value', None)
            if value.get('name').lower() == "humidity":
                humidity = value.get('value', None)
            if value.get('name').lower() == "temperature":
                temperature = value.get('value', None)

        print(
            "Executing query: INSERT INTO air (installation_id, datetime, pm1, pm10, pm25, "
            "temperature, pressure, humidity) "
            "VALUES ({0}, {1}, {2}, {3},"
            " {4}, {5}, {6}, {7});".format(iid, dt, pm1, pm10, pm25, temperature, pressure, humidity))
        cur.execute(
            "INSERT INTO air (installation_id, datetime, pm1, pm10, pm25, "
            "temperature, pressure, humidity) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s);",
            (iid, dt, pm1, pm10, pm25, temperature, pressure, humidity))


def insert_installations(cur, *args, **kwargs):
    latitude = kwargs.get('lat', None)
    longitude = kwargs.get('lon', None)
    max_dist = kwargs.get('max_dist', None)
    max_res = kwargs.get('max_res', None)

    installations = airly_reader.get_nearest_installations(latitude, longitude, max_dist=max_dist, max_res=max_res)

    for installation in installations:
        installation_id = installation.get('id')
        if db_get.get_installation_by_id(cur, installation_id) is None:
            insert_single_installation(cur, installation)


def insert_single_installation(cur, installation_info):
    installation_id = installation_info.get('id')
    location = installation_info.get('location')
    address = installation_info.get('address')

    address_id = insert_address(cur, location, address)

    elevation = installation_info.get('elevation')
    airly = installation_info.get('airly')

    print(
        "Executing query: INSERT INTO installation (installation_id, address_id, elevation, airly)"
        " VALUES ({0}, {1}, {2}, {3});".format(installation_id, address_id, elevation, airly))

    cur.execute("INSERT INTO installation (installation_id, address_id, elevation, airly) VALUES (%s, %s, %s, %s);",
                (installation_id, address_id, elevation, airly))


def insert_address(cur, location, address):
    latitude = location.get('latitude')
    longitude = location.get('longitude')
    country = address.get('country')
    city = address.get('city')
    street = address.get('street')
    st_number = address.get('number')

    lat_point = "{0:.2f}".format(latitude)
    lon_point = "{0:.2f}".format(longitude)

    point_id = insert_point(cur, lat_point, lon_point)

    address_id = db_get.get_address_id_by_coord(cur, latitude, longitude)

    if address_id is None:
        print(
            "Executing query: INSERT INTO address (point_id, latitude, longitude, "
            "country, city, street, st_number) "
            "VALUES ({0}, {1}, {2}, {3},"
            " {4}, {5}, {6});".format(point_id, latitude, longitude, country, city, street, st_number))
        cur.execute(
            "INSERT INTO address (point_id, latitude, longitude, "
            "country, city, street, st_number) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s);",
            (point_id, latitude, longitude, country, city, street, st_number))

    return db_get.get_address_id_by_coord(cur, latitude, longitude)
