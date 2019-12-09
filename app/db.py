from . import models
from . import util
from . import consts
from . import prediction
from . import mock
from dbservice.database.readers import reader
from datetime import datetime

# fetch all addresses within radius from (lat, lon) point using geo location distance algorithm
# returns result in form of Address list
def get_addresses_within_area(lat, lon, radius):
    all_addresses = reader.get_addresses()
    filtered_addresses = list(filter(lambda address: util.geo_location_distance(address[1], address[2], lat, lon) < radius, all_addresses))
    addresses = list(map(lambda address: models.Address(address[0], address[1], address[2]), filtered_addresses))
    
    return addresses

def is_address_supported(addr, radius):
    try:
        lat, lon = util.get_geo_location(addr)
        if not lat or not lon:
            return False
        all_addresses = reader.get_addresses()
        filtered_addresses = list(filter(lambda address: util.geo_location_distance(address[1], address[2], lat, lon) < radius, all_addresses))
        addresses = list(map(lambda address: models.Address(address[0], address[1], address[2]), filtered_addresses))

        return len(addresses) > 0
    except:
        return False

def is_location_supported(lat, lon, radius):
    all_addresses = reader.get_addresses()
    filtered_addresses = list(filter(lambda address: util.geo_location_distance(address[1], address[2], lat, lon) < radius, all_addresses))
    addresses = list(map(lambda address: models.Address(address[0], address[1], address[2]), filtered_addresses))

    return len(addresses) > 0

# returns analysis data based on given GenerationParameters
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

    if consts.ENABLE_MOCK_DATA:
        data = mock.get_mock_data(date_from, date_to)
    else:
        # get analysis data
        air_data = get_air_data(addresses, date_from, date_to, air_columns, lat, lon, radius)
        weather_data = get_weather_data(addresses, date_from, date_to, weather_columns, lat, lon, radius)
        # combine data
        for k, v in air_data.items():
            data[k] = v
        for k, v in weather_data.items():
            data[k] = v

    data = util.interpolate_data(data, date_from, date_to)

    # fill information data
    data['info'] = get_analysis_data_info(addresses, lat, lon, radius)
    data['pm25_norm'] = consts.PM25_WHO_NORM
    data['pm10_norm'] = consts.PM10_WHO_NORM

    return data

# returns prediction data based on given GenerationParameters
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

    calc_fbprophet = parameters.calc_fbprophet
    calc_arima = parameters.calc_arima

    if consts.ENABLE_MOCK_DATA:
        historical_data = mock.get_mock_data(date_from, datetime.now())
        if consts.ENABLE_HEAVY_COMPUTING:
            if calc_fbprophet:
                fbprophet_data = mock.get_mock_data(datetime.now(), date_to)
            else:
                fbprophet_data = None
        linreg_data = mock.get_mock_data(datetime.now(), date_to)
        if calc_arima:
            arima_data = mock.get_mock_data(datetime.now(), date_to)
        else:
            arima_data = None
    else:
        # get past data
        air_data = get_air_data(addresses, consts.PREDICTION_PAST_DATA_START, datetime.now(), air_columns, lat, lon, radius)
        weather_data = get_weather_data(addresses, consts.PREDICTION_PAST_DATA_START, datetime.now(), weather_columns, lat, lon, radius)
        # combine data
        for k, v in air_data.items():
            past_data[k] = v
        for k, v in weather_data.items():
            past_data[k] = v

        if consts.ENABLE_HEAVY_COMPUTING:
            historical_data, fbprophet_data, linreg_data, arima_data = prediction.predict(past_data, date_from, date_to, calc_fbprophet, calc_arima)
        else:
            historical_data, linreg_data, arima_data = prediction.predict(past_data, date_from, date_to, calc_fbprophet, calc_arima)
    
    data = dict()
    data['historical'] = historical_data
    if consts.ENABLE_HEAVY_COMPUTING:
        data['fbprophet'] = fbprophet_data
    data['linreg'] = linreg_data
    data['arima'] = arima_data

    # fill information data
    data['info'] = get_prediction_data_info(addresses, lat, lon, radius)
    data['pm25_norm'] = consts.PM25_WHO_NORM
    data['pm10_norm'] = consts.PM10_WHO_NORM

    data['historical'] = util.interpolate_data(data['historical'], date_from, datetime.now())

    return data

def get_analysis_data_info(addresses, lat, lon, radius):
    info = []
    info.append(consts.ANALYSIS_POINTS_NUM_MESSAGE.format(len(addresses)))
    if len(addresses) < consts.ADDRESSES_WARNING_NUM:
        info.append(consts.ANALYSIS_INACCURATE_POINTS_NUM_LOW_WARNING)
    if 0 < addresses_weight(addresses, lat, lon, radius) < consts.ADDRESSES_WARNING_WEIGHT:
        info.append(consts.ANALYSIS_INACCURATE_POINTS_FAR_FROM_CENTER_WARNING)

    return info

def get_prediction_data_info(addresses, lat, lon, radius):
    info = []
    info.append(consts.PREDICTION_POINTS_NUM_MESSAGE.format(len(addresses)))
    if len(addresses) < consts.ADDRESSES_WARNING_NUM:
        info.append(consts.PREDICTION_INACCURATE_POINTS_NUM_LOW_WARNING)
    if 0 < addresses_weight(addresses, lat, lon, radius) < consts.ADDRESSES_WARNING_WEIGHT:
        info.append(consts.PREDICTION_INACCURATE_POINTS_FAR_FROM_CENTER_WARNING)

    return info

# returns empty data object, which is a dict, where keys are column names,
# and values are dicts of data for each column with datetime as a key and measurement value as value
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

# retrieves air data for given parameters
# performs data average using addresses
# performs data aggregation to given datetimes (00:00, 06:00 etc.)
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

    # average data
    data = get_averaged_data(data, lat, lon, radius)
    # sort it by date
    data = get_sorted_data(data)
    # aggregate to points with 6hr delta
    data = get_aggregated_data(data, date_from, date_to)

    return data

# retrieves weather data for given parameters
# performs data average using addresses
# performs data aggregation to given datetimes (00:00, 06:00 etc.)
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

    # average data
    data = get_averaged_data(data, lat, lon, radius)
    # sort it by date
    data = get_sorted_data(data)
    # aggregate to points with 6hr delta
    data = get_aggregated_data(data, date_from, date_to)

    return data

# returns averaged data for addresses so that a single measurement value for datetime is present
def get_averaged_data(data, lat, lon, radius):
    data_cpy = dict()
    for col in data.keys():
        data_cpy[col] = dict()
        for date, address_data in data[col].items():
            data_avg = data_average(address_data, lat, lon, radius)
            if data_avg != -1:
                data_cpy[col][date] = data_avg
    
    return data_cpy

# sorts data for each column by datetime
def get_sorted_data(data):
    data_cpy = dict()
    for col in data.keys():
        data_cpy[col] = dict()
        for date in sorted(data[col].keys()):
            data_cpy[col][date] = data[col][date]

    return data_cpy

# returns aggregated data to specific datetimes (00:00, 06:00 etc.) for whole data dict
def get_aggregated_data(data, date_from, date_to):
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

    return data_cpy

# retrieves data which should be aggregated to given aggregation datetime,
# that is data in (aggregation_datetime - consts.DATA_TIMEDELTA / 2, aggregation_datatime + consts.DATA_TIMEDELTA / 2) period
# then it is aggregated using weighted average, where weight is aggregation_datetime - measurement's datetime distance from aggreation_datetime 
def aggregate_data(data, aggregation_datetime):
    dates = list(map(lambda x: datetime.strptime(x, consts.DATE_FORMAT), data.keys()))
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

# averages data from multiple addresses to a single point using weighted average, where weight
# is radius - measurement's point distance from center
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

# calculated weight of address, where weight is center - distance from center
def addresses_weight(addresses, center_lat, center_lon, radius):
    sum_w = 0
    for address in addresses:
        distance = util.geo_location_distance(center_lat, center_lon, address.lat, address.lon)
        w = (radius - distance) / radius
        sum_w = sum_w + w

    return sum_w

# rounds datetime by setting seconds and microseconds to 0
def round_datetime(dt):
    return dt.replace(second=0, microsecond=0)

# prepares list of present air columns based on GenerationParameters
def prepare_air_columns(parameters):
    columns = []
    if parameters.is_pm1:
        columns.append('pm1')
    if parameters.is_pm25:
        columns.append('pm25')
    if parameters.is_pm10:
        columns.append('pm10')

    return columns

# prepares list of present weather columns based on GenerationParameters
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

# build query string between SELECT and FROM for data retrieve based on given columns
def prepare_columns_query_string(columns):
    if columns:
        return ', ' + ', '.join(columns)
    else:
        return ''