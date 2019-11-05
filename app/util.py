from . import consts
from . import models
from math import pi, sqrt, sin, cos, atan2, ceil
import requests
import datetime
import json

# creates GenerationParameters model from GenerateForm
def create_generation_parameters(form):
    address = form.cleaned_data.get('address')
    radius = float(form.cleaned_data.get('radius'))
    date_from = form.cleaned_data.get('date_from')
    date_to = form.cleaned_data.get('date_to')
    is_pm1 = form.cleaned_data.get('is_pm1')
    is_pm25 = form.cleaned_data.get('is_pm25')
    is_pm10 = form.cleaned_data.get('is_pm10')
    is_temp = form.cleaned_data.get('is_temp')
    is_pressure = form.cleaned_data.get('is_pressure')
    is_humidity = form.cleaned_data.get('is_humidity')
    is_wind = form.cleaned_data.get('is_wind')
    is_clouds = form.cleaned_data.get('is_clouds')

    return models.GenerationParameters(address, radius, date_from, date_to, is_pm1, is_pm25, is_pm10, is_temp, is_pressure, is_humidity, is_wind, is_clouds)

# creates GenerationParameters model for guest
def create_guest_generation_parameters(location):
    date_from = datetime.datetime.now() - datetime.timedelta(days=7)
    date_to = datetime.datetime.now() + datetime.timedelta(days=7)

    return models.GenerationParameters(location, 5.0, date_from, date_to, True, True, True, True, True, True, True, True)

# converts configuration data to GenerationParameters model
def convert_to_generation_parameters(configuration, for_prediction=False):
    address = configuration.address
    radius = float(configuration.radius)
    
    if for_prediction:
        date_from = datetime.datetime.now()
        date_to = datetime.datetime.now() + datetime.timedelta(days=float(configuration.period))
    else:
        date_from = datetime.datetime.now() - datetime.timedelta(days=float(configuration.period))
        date_to = datetime.datetime.now()

    is_pm1 = configuration.is_pm1
    is_pm25 = configuration.is_pm25
    is_pm10 = configuration.is_pm10
    is_temp = configuration.is_temp
    is_pressure = configuration.is_pressure
    is_humidity = configuration.is_humidity
    is_wind = configuration.is_wind
    is_clouds = configuration.is_clouds

    return models.GenerationParameters(address, radius, date_from, date_to, is_pm1, is_pm25, is_pm10, is_temp, is_pressure, is_humidity, is_wind, is_clouds)

def convert_from_generation_parameters(parameters):
    result = dict()
    result['address'] = parameters.address
    result['radius'] = parameters.radius
    result['date_from'] = str(parameters.date_from)
    result['date_to'] = str(parameters.date_to)
    result['is_pm1'] = parameters.is_pm1
    result['is_pm25'] = parameters.is_pm25
    result['is_pm10'] = parameters.is_pm10
    result['is_temp'] = parameters.is_temp
    result['is_pressure'] = parameters.is_pressure
    result['is_humidity'] = parameters.is_humidity
    result['is_wind'] = parameters.is_wind
    result['is_clouds'] = parameters.is_clouds

    return result

def convert_json_to_generation_parameters(parameters):
    address = parameters['address']
    radius = parameters['radius']
    date_from = datetime.datetime.strptime(normalize_date_string(parameters['date_from']), consts.DATE_FORMAT)
    date_to = datetime.datetime.strptime(normalize_date_string(parameters['date_to']), consts.DATE_FORMAT)
    is_pm1 = parameters['is_pm1']
    is_pm25 = parameters['is_pm25']
    is_pm10 = parameters['is_pm10']
    is_temp = parameters['is_temp']
    is_pressure = parameters['is_pressure']
    is_humidity = parameters['is_humidity']
    is_wind = parameters['is_wind']
    is_clouds = parameters['is_clouds']

    return models.GenerationParameters(address, radius, date_from, date_to, is_pm1, is_pm25, is_pm10, is_temp, is_pressure, is_humidity, is_wind, is_clouds)

# Measure distance between two locations - START

def deg_to_rad(deg):
    return deg * pi / 180

def geo_location_distance(lat1, lon1, lat2, lon2):
    earth_radius = 6371

    d_lat = deg_to_rad(lat2 - lat1)
    d_lon = deg_to_rad(lon2 - lon1)

    deg_lat1 = deg_to_rad(lat1)
    deg_lat2 = deg_to_rad(lat2)

    a = sin(d_lat / 2) * sin(d_lat/2) + sin(d_lon / 2) * sin(d_lon / 2) * cos(deg_lat1) * cos(deg_lat2)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return earth_radius * c

# Measure distance between two locations - END

# Get location based on address - START
api_token = '43cf3f75156b90'
api_base_url = 'https://eu1.locationiq.com/v1/search.php'

def get_geo_location(address):
    data = {
        'key': api_token,
        'q': address,
        'format': 'json'
    }

    response = requests.get(api_base_url, params=data)
    if response.status_code == 200:
        json_response = json.loads(response.content.decode('utf-8'))
        if isinstance(json_response, list):
            lat = float(json_response[0]['lat'])
            lon = float(json_response[0]['lon'])
            return lat, lon
        else:
            return None, None
    else:
        return None, None

# Get location based on address - END

def is_correct_address(address):
    data = {
        'key': api_token,
        'q': address,
        'format': 'json'
    }

    response = requests.get(api_base_url, params=data)
    if response.status_code == 200:
        json_response = json.loads(response.content.decode('utf-8'))
        if isinstance(json_response, list):
            try:
                lat = float(json_response[0]['lat'])
                lon = float(json_response[0]['lon'])
                return True
            except:
                return False
        else:
            return False
    else:
        return False

# gets first data aggregation datetime (which is 00:00, 06:00, 12:00 or 18:00) after date_from
# date_from can be both datetime or string, if it is string then it is converted to datetime
# using consts.DATE_FORMAT
def get_data_aggregation_starting_datetime(date_from):
    if isinstance(date_from, str):
        date_from = datetime.datetime.strptime(date_from, consts.DATE_FORMAT)
    starting_datetime = datetime.datetime(year=date_from.year, month=date_from.month, day=date_from.day)
    date_from_tzinfo_free = date_from.replace(tzinfo=None)
    while starting_datetime <= date_from_tzinfo_free:
        starting_datetime = starting_datetime + consts.DATA_TIMEDELTA

    return starting_datetime

# gets all aggregation datetimes between date_from and date_to,
# staring with result of get_data_aggregation_starting_datetime
# datetimes are calculated by adding consts.DATA_TIMEDELTA
# result is not a list of datetimes, but a list of timestamps,
# which was a requirement for linear regression, but this is expected to change
# when switched to a non-placeholder prediction algorithm
def get_prediction_datetimes(date_from, date_to):
    dt = get_data_aggregation_starting_datetime(date_from)
    date_to_tzinfo_free = date_to.replace(tzinfo=None)
    datetimes = []
    while dt <= date_to_tzinfo_free:
        datetimes.append(dt)
        dt = dt + consts.DATA_TIMEDELTA

    datetimes = list(map(lambda x: datetime.datetime.timestamp(x), datetimes))

    return datetimes

def get_chart_title(location, date_from, date_to):
    return "Examination for {0}, {1} to {2}".format(location, date_from.date(), date_to.date())

def get_examination_filename(location, date_from, date_to):
    return "RQA {0} {1} {2}".format(location, date_from.date(), date_to.date())

def extract_factor_data(data):
    result = dict()
    for column in consts.AIR_COLUMNS:
        if column in data:
            result[column] = data[column]
    for column in consts.WEATHER_COLUMNS:
        if column in data:
            result[column] = data[column]
    
    return result

def get_factor_name(factor):
    return consts.COLUMNS_NAMES[factor]

def is_configuration_incomplete(configuration):
    return not (is_specified(configuration.address) and is_specified(configuration.radius) and is_specified(configuration.period))

def is_specified(s):
    return not (s is None or s == "")

def is_positive_number(s):
    try:
        float(s)
        return float(s) > 0
    except ValueError:
        return False

def normalize_date_string(date):
    date = date.split('+')[0]
    date = date.split('.')[0]

    return date
    
def convert_to_past_data_with_datetimes(past_data):
    result = dict()
    for col in past_data.keys():
        result[col] = dict()
        for date_as_string, value in past_data[col].items():
            result[col][datetime.datetime.strptime(date_as_string, consts.DATE_FORMAT)] = value

    return result

def convert_to_past_data_with_strings(past_data):
    result = dict()
    for col in past_data.keys():
        result[col] = dict()
        for date_as_datetime, value in past_data[col].items():
            result[col][date_as_datetime.strftime(consts.DATE_FORMAT)] = value

    return result

def get_prediction_periods(date_to):
    now = datetime.datetime.now()
    delta = date_to - now
    periods = delta / datetime.timedelta(hours=6)

    return int(periods)

def get_prediction_offset(date_from):
    now = datetime.datetime.now()
    if now < date_from:
        return 0
        
    delta = now - date_from
    offset = delta / datetime.timedelta(hours=6)

    return int(ceil(offset)) - 1

def interpolate_data(data, date_from, date_to):
    result = dict()
    for col in data.keys():
        result[col] = dict()
        interpolation_date = get_data_aggregation_starting_datetime(date_from)
        while interpolation_date < date_to:
            if interpolation_date.strftime(consts.DATE_FORMAT) in data[col].keys():
                result[col][interpolation_date.strftime(consts.DATE_FORMAT)] = data[col][interpolation_date.strftime(consts.DATE_FORMAT)]
            else:
                result[col][interpolation_date.strftime(consts.DATE_FORMAT)] = None
            interpolation_date = interpolation_date + datetime.timedelta(hours=6)

    return result
            