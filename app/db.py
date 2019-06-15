from . import models
from . import util
from . import consts
from dbservice.database.readers import reader

def get_addresses_within_area(lat, lon, radius):
    all_addresses = reader.get_addresses()
    filtered_addresses = list(filter(lambda address: util.geo_location_distance(address[1], address[2], lat, lon) < radius, all_addresses))
    addresses = list(map(lambda address: models.Address(address[0], address[1], address[2]), filtered_addresses))
    print("Found {0} of {1} addresses in given area.".format(len(filtered_addresses), len(all_addresses)))
    print("Returning {0} addresses.".format(len(addresses)))
    
    return addresses

def get_analysis_data(parameters):
    # convert address to coordinates
    lat, lon = util.get_geo_location(parameters.address)
    # get other parameters
    radius = parameters.radius
    date_from = parameters.date_from
    date_to = parameters.date_to
    # get installation within given radius based on coordinates
    addresses = get_addresses_within_area(lat, lon, radius)
    # get air columns
    air_columns = prepare_air_columns(parameters)
    # get weather columns
    weather_columns = prepare_weather_columns(parameters)
    # create data object
    data = empty_analysis_data()

    # get analysis data
    air_data = get_air_data(addresses, date_from, date_to, air_columns, lat, lon, radius)
    weather_data = get_weather_data(addresses, date_from, date_to, weather_columns, lat, lon, radius)
    # combine data
    for k, v in air_data.items():
        data[k] = v
    for k, v in weather_data.items():
        data[k] = v

    # fill information data
    data['info'] = []
    data['info'].append('Analysis based on {} point(s) in given area.'.format(len(addresses)))
    if len(addresses) < consts.ADDRESSES_WARNING_NUM:
        data['info'].append('Analysis may be inaccurate due to low point number in area.')
    if 0 < addresses_weight(addresses, lat, lon, radius) < consts.ADDRESSES_WARNING_WEIGHT:
        data['info'].append('Analysis may be inaccurate due to points being far from area center.')
    # fill WHO norms for PM25 and PM10
    data['pm25_norm'] = consts.PM25_WHO_NORM
    data['pm10_norm'] = consts.PM10_WHO_NORM

    return data

def empty_analysis_data():
    data = dict()
    data['pm1'] = dict()
    data['pm25'] = dict()
    data['pm10'] = dict()
    data['temperature'] = dict()
    data['pressure'] = dict()
    data['humidity'] = dict()
    data['wind_speed'] = dict()
    data['wind_degree'] = dict()
    data['clouds'] = dict()

    return data

def get_air_data(addresses, date_from, date_to, columns, lat, lon, radius):
    data = dict()
    for address in addresses:
        data_for_address = reader.get_air_readings_for_address(address.id, date_from, date_to, ', '.join(columns))
        for col in range(len(columns)):
            data_to_average = dict()
            for record in data_for_address:
                if not str(round_datetime(record[0])) in data_to_average:
                    data_to_average[str(round_datetime(record[0]))] = []
                data_to_average[str(round_datetime(record[0]))].append((address, record[col+1]))

            data_averaged = dict()
            for date, values in data_to_average.items():
                data_averaged[date] = data_average(values, lat, lon, radius)

            data[columns[col]] = data_averaged

    return data

def get_weather_data(addresses, date_from, date_to, columns, lat, lon, radius):
    data = dict()
    for address in addresses:
        data_for_address = reader.get_weather_readings_for_address(address.id, date_from, date_to, ', '.join(columns))
        for col in range(len(columns)):
            data_to_average = dict()
            for record in data_for_address:
                if not str(round_datetime(record[0])) in data_to_average:
                    data_to_average[str(round_datetime(record[0]))] = []
                data_to_average[str(round_datetime(record[0]))].append((address, record[col+1]))

            data_averaged = dict()
            for date, values in data_to_average.items():
                data_averaged[date] = data_average(values, lat, lon, radius)

            data[columns[col]] = data_averaged

    return data

def data_average(address_data, center_lat, center_lon, radius):
    sum_w_data = 0
    sum_w = 0
    for (address, data) in address_data:
        if data is not None:
            distance = util.geo_location_distance(center_lat, center_lon, address.lat, address.lon)
            w = (radius - distance) / radius
            sum_w_data = sum_w_data + w * float(data)
            sum_w = sum_w + w

    if sum_w == 0:
        return 0
    else:
        return sum_w_data / sum_w

def addresses_weight(addresses, center_lat, center_lon, radius):
    sum_w = 0
    for address in addresses:
        distance = util.geo_location_distance(center_lat, center_lon, address.lat, address.lon)
        w = (radius - distance) / radius
        sum_w = sum_w + w

    return sum_w

def round_datetime(dt):
    return dt.replace(second=0, microsecond=0)

def prepare_air_columns(parameters):
    columns = []
    if parameters.is_pm1:
        columns.append('pm1')
    if parameters.is_pm25:
        columns.append('pm25')
    if parameters.is_pm10:
        columns.append('pm10')

    return columns

def prepare_weather_columns(parameters):
    columns = []
    if parameters.is_temp:
        columns.append('temperature')
    if parameters.is_pressure:
        columns.append('pressure')
    if parameters.is_humidity:
        columns.append('humidity')
    if parameters.is_wind:
        columns.append('wind_speed')
        columns.append('wind_degree')
    if parameters.is_clouds:
        columns.append('clouds')

    return columns