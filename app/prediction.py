from . import consts
from . import db
from . import util
from datetime import datetime
import numpy as np
from sklearn.linear_model import LinearRegression

# calculates prediction data from date_from to date_to using past_data
# after the process, cuts the (< date_from) part of predicted data so that
# only datetimes between date_from and date_to are present in the result
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
            if datetime.strptime(date, consts.DATE_FORMAT) >= date_from_tzinfo_free:
                data_cpy[col][date] = data[col][date]

    data = data_cpy

    return data

# calculates prediction data using linear regression
# calculations are performed for each column (PM1 etc.) separately
# specific datetimes (00:00, 06:00 etc.) are used
# note that past data is also included in result
def calculate_placeholder_prediction_data(past_data, date_to):
    for col in past_data.keys():
        if len(list(past_data[col].keys())) > 0:
            x = np.array(list(map(lambda x: datetime.timestamp(datetime.strptime(x, consts.DATE_FORMAT)), list(past_data[col].keys())))).reshape((-1, 1))
            y = np.array(list(past_data[col].values()))
            model = LinearRegression().fit(x, y)
            x_pred = np.array(util.get_prediction_datetimes(list(past_data[col].keys())[-1], date_to)).reshape((-1, 1))
            y_pred = model.predict(x_pred)
            for i in range(x_pred.size):
                past_data[col][str(datetime.fromtimestamp(x_pred.item(i)))] = y_pred.item(i)

    return past_data