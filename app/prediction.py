from . import consts
from . import db
from datetime import datetime

def predict(past_data, date_to):
    # create empty prediction data object
    data = db.empty_data()

    # calculate prediction data
    # TODO PLACEHOLDER
    data = calculate_placeholder_prediction_data(past_data, date_to)

    return data

def calculate_placeholder_prediction_data(past_data, date_to):
    print(str(past_data))

    for col in past_data.keys():
        if col in consts.AIR_COLUMNS:
            pass
        elif col in consts.WEATHER_COLUMNS:
            pass

    return db.empty_data()

def calculate_regression_for_air(col, past_data):
    pass

def calculate_regression_for_weather(col, past_data):
    pass