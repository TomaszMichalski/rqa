from . import consts
from . import models
from math import pi, sqrt, sin, cos, atan2
import requests
import datetime
import json

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

def get_data_aggregation_starting_datetime(date_from):
    if isinstance(date_from, str):
        date_from = datetime.datetime.strptime(date_from, '%Y-%m-%d %H:%M:%S')
    starting_datetime = datetime.datetime(year=date_from.year, month=date_from.month, day=date_from.day)
    date_from_tzinfo_free = date_from.replace(tzinfo=None)
    while starting_datetime <= date_from_tzinfo_free:
        starting_datetime = starting_datetime + consts.DATA_TIMEDELTA

    return starting_datetime

def get_prediction_datetimes(date_from, date_to):
    dt = get_data_aggregation_starting_datetime(date_from)
    date_to_tzinfo_free = date_to.replace(tzinfo=None)
    datetimes = []
    while dt <= date_to_tzinfo_free:
        datetimes.append(dt)
        dt = dt + consts.DATA_TIMEDELTA

    datetimes = list(map(lambda x: datetime.datetime.timestamp(x), datetimes))

    return datetimes