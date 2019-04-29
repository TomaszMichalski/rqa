from . import models
from math import pi, sqrt, sin, cos, atan2

def create_generation_parameters(form):
    address = form.cleaned_data.get('address')
    radius = form.cleaned_data.get('radius')
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

def deg_to_rad(deg):
    return deg * math.pi / 180

# Haversine formula
def geo_location_distance(lat1, lon1, lat2, lon2):
    earth_radius = 6371

    d_lat = deg_to_rad(lat2 - lat1)
    d_lon = deg_to_rad(lon2 - lon1)

    deg_lat1 = deg_to_rad(lat1)
    deg_lat2 = deg_to_rad(lat2)

    a = math.sin(d_lat / 2) * math.sin(d_lat/2) + math.sin(d_lon / 2) * math.sin(d_lon / 2) * math.cos(deg_lat1) * math.cos(deg_lat2)
    c = 2 * math.atan2(Math.sqrt(a), Math.sqrt(1 - a))

    return earth_radius * c

def get_installations_within_area(lat, lon, radius):
    # TODO
    #get installations from db-service into Installation objects
    #filter for get_location_distance < radius
    #return the result list
    return []