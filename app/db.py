from . import models
from . import util
from . import consts
from . import prediction
from dbservice.database.readers import reader
from datetime import datetime

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
    data = empty_data()

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

def get_prediction_data(parameters):
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
    # create past data object
    past_data = empty_data()

    # get past data
    air_data = get_air_data(addresses, consts.PREDICTION_PAST_DATA_START, datetime.now(), air_columns, lat, lon, radius)
    weather_data = get_weather_data(addresses, consts.PREDICTION_PAST_DATA_START, datetime.now(), weather_columns, lat, lon, radius)
    # combine data
    for k, v in air_data.items():
        past_data[k] = v
    for k, v in weather_data.items():
        past_data[k] = v

    data = prediction.predict(past_data, date_from, date_to)

    # fill information data
    data['info'] = []
    data['info'].append('Prediction based on {} point(s) in given area.'.format(len(addresses)))
    if len(addresses) < consts.ADDRESSES_WARNING_NUM:
        data['info'].append('Prediction may be inaccurate due to low point number in area.')
    if 0 < addresses_weight(addresses, lat, lon, radius) < consts.ADDRESSES_WARNING_WEIGHT:
        data['info'].append('Prediction may be inaccurate due to points being far from area center.')
    # fill WHO norms for PM25 and PM10
    data['pm25_norm'] = consts.PM25_WHO_NORM
    data['pm10_norm'] = consts.PM10_WHO_NORM

    return data

def empty_data():
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
    for col in columns:
        data[col] = dict()

    for address in addresses:
        data_for_address = reader.get_air_readings_for_address(address.id, date_from, date_to, prepare_columns_query_string(columns))
        for col_i in range(len(columns)):
            for record in data_for_address:
                if not str(round_datetime(record[0])) in data[columns[col_i]]:
                    data[columns[col_i]][str(round_datetime(record[0]))] = []
                data[columns[col_i]][str(round_datetime(record[0]))].append((address, record[col_i+1]))

    data_cpy = dict()
    for col in data.keys():
        data_cpy[col] = dict()
        for date, address_data in data[col].items():
            data_avg = data_average(address_data, lat, lon, radius)
            if data_avg != -1:
                data_cpy[col][date] = data_avg

    data = data_cpy

    data_cpy = dict()
    for col in data.keys():
        data_cpy[col] = dict()
        for date in sorted(data[col].keys()):
            data_cpy[col][date] = data[col][date]

    data = data_cpy

    data_cpy = dict()
    date_to_tzinfo_free = date_to.replace(tzinfo=None)
    for col in data.keys():
        data_cpy[col] = dict()
        aggregation_datetime = util.get_data_aggregation_starting_datetime(date_from)
        while aggregation_datetime < date_to_tzinfo_free:
            aggregated_data = aggregate_data(data[col], aggregation_datetime)
            if aggregated_data != -1:
                data_cpy[col][str(aggregation_datetime)] = aggregated_data
            aggregation_datetime = aggregation_datetime + consts.DATA_TIMEDELTA

    data = data_cpy

    return data

def get_weather_data(addresses, date_from, date_to, columns, lat, lon, radius):
    data = dict()
    for col in columns:
        data[col] = dict()

    for address in addresses:
        data_for_address = reader.get_weather_readings_for_address(address.id, date_from, date_to, prepare_columns_query_string(columns))
        for col_i in range(len(columns)):
            for record in data_for_address:
                if not str(round_datetime(record[0])) in data[columns[col_i]]:
                    data[columns[col_i]][str(round_datetime(record[0]))] = []
                data[columns[col_i]][str(round_datetime(record[0]))].append((address, record[col_i+1]))

    data_cpy = dict()
    for col in data.keys():
        data_cpy[col] = dict()
        for date, address_data in data[col].items():
            data_avg = data_average(address_data, lat, lon, radius)
            if data_avg != -1:
                data_cpy[col][date] = data_avg

    data = data_cpy

    data_cpy = dict()
    for col in data.keys():
        data_cpy[col] = dict()
        for date in sorted(data[col].keys()):
            data_cpy[col][date] = data[col][date]

    data = data_cpy

    data_cpy = dict()
    date_to_tzinfo_free = date_to.replace(tzinfo=None)
    for col in data.keys():
        data_cpy[col] = dict()
        aggregation_datetime = util.get_data_aggregation_starting_datetime(date_from)
        while aggregation_datetime < date_to_tzinfo_free:
            aggregated_data = aggregate_data(data[col], aggregation_datetime)
            if aggregated_data != -1:
                data_cpy[col][str(aggregation_datetime)] = aggregated_data
            aggregation_datetime = aggregation_datetime + consts.DATA_TIMEDELTA

    data = data_cpy

    return data

def aggregate_data(data, aggregation_datetime):
    dates = list(map(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'), data.keys()))
    dates = list(filter(lambda x: x > aggregation_datetime - consts.DATA_TIMEDELTA / 2 and x < aggregation_datetime + consts.DATA_TIMEDELTA / 2, dates))
    aggregated_data_sum = 0
    aggregated_data_weight = 0
    for date in dates:
        temp_weight = (consts.DATA_TIMEDELTA / 2 - abs(aggregation_datetime - date)) / (consts.DATA_TIMEDELTA / 2)
        aggregated_data_sum = aggregated_data_sum + temp_weight * data[str(date)]
        aggregated_data_weight = aggregated_data_weight + temp_weight

    if aggregated_data_weight == 0:
        return -1
    else:
        return aggregated_data_sum / aggregated_data_weight

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
        return -1
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

def prepare_columns_query_string(columns):
    if columns:
        return ', ' + ', '.join(columns)
    else:
        return ''