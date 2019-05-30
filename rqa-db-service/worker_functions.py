# worker_functions.py
from datetime import datetime

from api import airly_reader, owm_reader
from database.getters.misc import get_coordinates_for_each_address, get_airly_installation_ids, get_address_id_for_installation_id
from database.insertions import air, weather

weather_apis = ['open_weather', 'airly']
air_apis = ['airly']


def retrieve_and_insert_readings_for_all_addresses(cur):
    addresses = get_coordinates_for_each_address(cur)
    retrieve_and_insert_air_readings(cur, addresses)
    retrieve_and_insert_weather_readings(cur, addresses)


def retrieve_and_insert_weather_readings(cur, addresses):
    for api in weather_apis:
        if api == 'open_weather':
            retrieve_and_insert_openweather_weather_readings(cur, addresses)
        if api == 'airly':
            retrieve_and_insert_airly_weather_readings(cur)


def retrieve_and_insert_air_readings(cur, addresses):
    for api in air_apis:
        if api == 'airly':
            retrieve_and_insert_airly_air_readings(cur)


def retrieve_and_insert_openweather_weather_readings(cur, addresses):
    for address in addresses:
        address_id = address[0]
        latitude = address[1]
        longitude = address[2]
        conditions = owm_reader.get_conditions(latitude, longitude)

        if conditions is not None:
            weather_info = conditions.get('weather')
            weather_desc = ""
            for info in weather_info:
                weather_desc += info.get('description') + '/'
            weather_desc = weather_desc[0:-1]

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

            weather.insert_single_weather_reading(cur, address_id, dt, "open_weather", weather=weather_desc,
                                                  temperature=temperature, pressure=pressure, humidity=humidity,
                                                  temp_min=temp_min, temp_max=temp_max, wind_speed=wind_speed,
                                                  wind_degree=wind_degree, clouds=clouds)


def retrieve_and_insert_airly_air_readings(cur):
    installation_ids = get_airly_installation_ids(cur)
    for installation_id in installation_ids:
        iid = installation_id[0]
        air_data = airly_reader.get_measurements(iid)
        if air_data is not None:
            pm1 = pm10 = pm25 = None
            current = air_data.get('current')
            raw_dt = current.get('tillDateTime')
            dt = raw_dt[0:10] + ' ' + raw_dt[11:19]
            values = current.get('values')
            for value in values:
                if value.get('name').lower() == "pm1":
                    pm1 = value.get('value', None)
                if value.get('name').lower() == "pm10":
                    pm10 = value.get('value', None)
                if value.get('name').lower() == "pm25":
                    pm25 = value.get('value', None)

            address_id = get_address_id_for_installation_id(cur, iid)
            address_id = address_id[0]
            air.insert_single_air_reading(cur, address_id, dt, "airly", pm1=pm1, pm10=pm10, pm25=pm25)


def retrieve_and_insert_airly_weather_readings(cur):
    installation_ids = get_airly_installation_ids(cur)
    for installation_id in installation_ids:
        iid = installation_id[0]
        air_data = airly_reader.get_measurements(iid)
        if air_data is not None:
            temperature = pressure = humidity = None
            current = air_data.get('current')
            raw_dt = current.get('tillDateTime')
            dt = raw_dt[0:10] + ' ' + raw_dt[11:19]
            values = current.get('values')
            for value in values:
                if value.get('name').lower() == "temperature":
                    temperature = value.get('value', None)
                if value.get('name').lower() == "pressure":
                    pressure = value.get('value', None)
                if value.get('name').lower() == "humidity":
                    humidity = value.get('value', None)

            address_id = get_address_id_for_installation_id(cur, iid)
            address_id = address_id[0]
            weather.insert_single_weather_reading(cur, address_id, dt, "airly",
                                                  temperature=temperature, pressure=pressure, humidity=humidity)
