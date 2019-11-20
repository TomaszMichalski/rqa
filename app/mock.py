import random
import datetime
from . import util
from . import consts

MOCK_BOUNDARY_VALUES = {
    'pm1': [0.0, 100.0],
    'pm25': [0.0, 100.0],
    'pm10': [0.0, 100.0],
    'temperature': [5.0, 25.0],
    'pressure': [980.0, 1020.0],
    'humidity': [0.0, 100.0],
    'wind_speed': [0.0, 5.0],
    'wind_degree': [0.0, 360.0],
    'clouds': [0.0, 100.0]
}

def get_mock_data(date_from, date_to):
    data = dict()
    for col in MOCK_BOUNDARY_VALUES.keys():
        data[col] = dict()
        date = util.get_data_aggregation_starting_datetime(date_from)
        while date < date_to:
            data[col][date.strftime(consts.DATE_FORMAT)] = get_random_value(col)
            date = date + datetime.timedelta(hours=6)

    return data

def get_random_value(col):
    return random.uniform(MOCK_BOUNDARY_VALUES[col][0], MOCK_BOUNDARY_VALUES[col][1])
