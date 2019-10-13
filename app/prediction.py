from . import consts
from . import db
from . import util
from datetime import datetime
import numpy as np
from sklearn.linear_model import LinearRegression
import pandas as pd
from fbprophet import Prophet

# calculates prediction data from date_from to date_to using past_data
# after the process, cuts the (< date_from) part of predicted data so that
# only datetimes between date_from and date_to are present in the result
def predict(past_data, date_from, date_to):
    # create empty prediction data object
    data = db.empty_data()

    # calculate prediction data
    data = calculate_prediction_data(past_data, date_to)

    result = db.empty_data()
    now = datetime.now()
    for col in data.keys():
        for date in data[col].keys():
            if datetime.strptime(date, consts.DATE_FORMAT) >= now:
                result[col][date] = data[col][date]
        for date in past_data[col].keys():
            if datetime.strptime(date, consts.DATE_FORMAT) >= date_from:
                result[col][date] = past_data[col][date]

    result = get_sorted_data(result)

    return result

def calculate_prediction_data(past_data, date_to):
    print("Converting data")
    data = util.convert_to_past_data_with_datetimes(past_data)
    print("Done")
    for col in past_data.keys():
        if len(list(past_data[col].keys())) > 0:
            print("Starting prediction for column {}".format(col))
            m = Prophet(weekly_seasonality=True)
            df = pd.DataFrame(list(data[col].items()), columns=['ds', 'y'])
            m.fit(df)
            future = m.make_future_dataframe(periods=util.get_prediction_periods(date_to), freq='6H')
            forecast = m.predict(future)
            for index, row in forecast.iterrows():
                data[col][row['ds']] = row['yhat']
            print("Finished prediction for column {}".format(col))

    data = util.convert_to_past_data_with_strings(data)
    return data

def get_sorted_data(data):
    data_cpy = dict()
    for col in data.keys():
        data_cpy[col] = dict()
        for date in sorted(data[col].keys()):
            data_cpy[col][date] = data[col][date]

    return data_cpy