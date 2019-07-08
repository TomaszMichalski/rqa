from . import consts
from . import db
from . import util
from datetime import datetime
import numpy as np
from sklearn.linear_model import LinearRegression

def predict(past_data, date_from, date_to):
    # create empty prediction data object
    data = db.empty_data()

    # calculate prediction data
    # TODO PLACEHOLDER
    data = calculate_placeholder_prediction_data(past_data, date_to)

    data_cpy = dict()
    date_from_tzinfo_free = date_from.replace(tzinfo=None)
    for col in data.keys():
        data_cpy[col] = dict()
        for date in data[col].keys():
            if datetime.strptime(date, '%Y-%m-%d %H:%M:%S') >= date_from_tzinfo_free:
                data_cpy[col][date] = data[col][date]

    data = data_cpy

    return data

def calculate_placeholder_prediction_data(past_data, date_to):
    for col in past_data.keys():
        if len(list(past_data[col].keys())) > 0:
            x = np.array(list(map(lambda x: datetime.timestamp(datetime.strptime(x, '%Y-%m-%d %H:%M:%S')), list(past_data[col].keys())))).reshape((-1, 1))
            y = np.array(list(past_data[col].values()))
            model = LinearRegression().fit(x, y)
            x_pred = np.array(util.get_prediction_datetimes(list(past_data[col].keys())[-1], date_to)).reshape((-1, 1))
            y_pred = model.predict(x_pred)
            print(str(x_pred.size))
            print(str(y_pred.size))
            for i in range(x_pred.size):
                print(str(i))
                past_data[col][str(datetime.fromtimestamp(x_pred.item(i)))] = y_pred.item(i)

    return past_data