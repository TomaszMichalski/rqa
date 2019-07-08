from datetime import timedelta

ADDRESSES_WARNING_NUM = 5
ADDRESSES_WARNING_WEIGHT = 0.5

PM25_WHO_NORM = 25
PM10_WHO_NORM = 50

PREDICTION_PAST_DATA_START = '2019-06-01 00:00:00'

AIR_COLUMNS = ['pm1', 'pm25', 'pm10']
WEATHER_COLUMNS = ['temperature', 'pressure', 'humidity', 'wind_speed', 'wind_degree', 'clouds']

DATA_TIMEDELTA = timedelta(hours=6)