from . import models
from . import util
from . import consts

def get_installations_within_area(lat, lon, radius):
    # TODO
    #get installations from db-service into Installation objects
    #filter for get_location_distance < radius
    #return the result list
    return []

def get_analysis_data(parameters):
    # convert address to coordinates
    lat, lon = util.get_geo_location(parameters.address)
    # get installation within given radius based on coordinates
    installations = get_installations_within_area(lat, lon, parameters.radius)
    # create data object
    data = dict()
    # fill data based on form fields
    if parameters.is_pm1:
        data['pm1'] = get_air_data(installations, parameters.date_from, parameters.date_to, 'pm1')
    if parameters.is_pm25:
        data['pm25'] = get_air_data(installations, parameters.date_from, parameters.date_to, 'pm25')
    if parameters.is_pm10:
        data['pm10'] = get_air_data(installations, parameters.date_from, parameters.date_to, 'pm10')
    if parameters.is_temp:
        data['temp'] = get_weather_data(installations, parameters.date_from, parameters.date_to, 'temperature')
    if parameters.is_pressure:
        data['pressure'] = get_weather_data(installations, parameters.date_from, parameters.date_to, 'pressure')
    if parameters.is_humidity:
        data['humidity'] = get_weather_data(installations, parameters.date_from, parameters.date_to, 'humidity')
    if parameters.is_wind:
        data['wind_speed'] = get_weather_data(installations, parameters.date_from, parameters.date_to, 'wind_speed')
        data['wind_degree'] = get_weather_data(installations, parameters.date_from, parameters.date_to, 'wind_degree')
    if parameters.is_clouds:
        data['clouds'] = get_weather_data(installations, parameters.date_from, parameters.date_to, 'clouds')
    # fill information data
    data['info'] = []
    data['info'].append('Analysis based on {} installation(s) in given area.'.format(len(installations)))
    if len(installations) < consts.INSTALLATIONS_WARNING_NUM:
        data['info'].append('Analysis may be inaccurate due to low installations number in area.')
    if installation_weight(installations, lat, lon, parameters.radius) < consts.INSTALLATIONS_WARNING_WEIGHT:
        data['info'].append('Analysis may be inaccurate due to installations being far from area center.')
    # fill WHO norms for PM25 and PM10
    data['pm25_norm'] = consts.PM25_WHO_NORM
    data['pm10_norm'] = consts.PM10_WHO_NORM

    return data

def get_air_data(installations, date_from, date_to, column):
    # TODO
    # get specific column for given Installation IDs
    # group measurements by datetime
    # average each group with data_average
    return dict()

def get_weather_data(installations, date_from, date_to, column):
    # TODO
    # get specific column for given Installation IDs
    # group measurements by datetime
    # average each group with data_average
    return dict()

def data_average(installation_data, center_lat, center_lon, radius):
    sum_w_data = 0
    sum_w = 0
    for installation, data in installation_data.items():
        distance = geo_location_distance(center_lat, center_lon, installation.lat, installation.lon)
        w = (radius - distance) / radius
        sum_w_data = sum_w_data + w * data
        sum_w = sum_w + w

    return sum_w_data / sum_w

def installation_weight(installations, center_lat, center_lon, radius):
    sum_w = 0
    for i in installations:
        distance = geo_location_distance(center_lat, center_lon, installation.lat, installation.lon)
        w = (radius - distance) / radius
        sum_w = sum_w + w

    return sum_w