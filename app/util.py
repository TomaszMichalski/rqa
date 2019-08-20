from . import consts
from . import models
from math import pi, sqrt, sin, cos, atan2
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
            return None
    else:
        return None

# Get location based on address - END

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