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
    for col in data.keys():
        for date in data[col].keys():
            if datetime.strptime(date, consts.DATE_FORMAT) >= date_from:
                result[col][date] = data[col][date]

    result = get_sorted_data(result)

    return result

def calculate_prediction_data(past_data, date_to):
    print("Converting data")
    data = util.convert_to_past_data_with_datetimes(past_data)
    print("Done")
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    for col in consts.PREDICTION_ORDER:
        if len(list(past_data[col].keys())) > 0:
            print("Starting prediction for column {}".format(col))
            # m = Prophet(weekly_seasonality=True, daily_seasonality=True, growth='logistic')
            m = Prophet(growth = 'logistic')
            df = pd.DataFrame(list(data[col].items()), columns=['ds', 'y'])
            # df = merge_regressors(df, get_pre_predicted_regressors_df(data, col))
            df = add_regressors_data(df, data, col)
            df = df.interpolate(method='linear')
            df = apply_cap_floor(df, col)
            m = add_regressors(m, col)
            m.fit(df)
            future = m.make_future_dataframe(periods=util.get_prediction_periods(date_to), freq='6H')
            future = add_regressors_data(future, data, col)
            future = future.interpolate(method='linear')
            future = apply_cap_floor(future, col)
            forecast = m.predict(future)
            now = datetime.now()
            for index, row in forecast.iterrows():
                if row['ds'] >= now:
                    data[col][row['ds']] = row['yhat']
            print("Finished prediction for column {}".format(col))

    data = util.convert_to_past_data_with_strings(data)
    return data

def apply_cap_floor(df, col):
    if col in consts.FLOOR_ZERO_COLUMNS:
        df['floor'] = 0
    if col == 'wind_degree':
        df['cap'] = 360
    elif col == 'humidity':
        df['cap'] = 100
    else:
        df['cap'] = consts.MAX_CAP

    return df

def add_regressors_data(df, data, column):
    regressors = get_pre_predicted_columns(column)
    for col in regressors:
        df[col] = df['ds'].apply(get_regressor_applicative, args=(col, data,))

    df.reset_index(drop=True)
    return df

def get_pre_predicted_columns(column):
    column_pos = consts.PREDICTION_ORDER.index(column)

    return consts.PREDICTION_ORDER[:column_pos]

def add_regressors(m, column):
    regressors_names = get_pre_predicted_columns(column)
    for col in regressors_names:
        m.add_regressor(col, prior_scale=0.5, mode='multiplicative')

    return m

def get_regressor_applicative(ds, column, data):
    date = pd.to_datetime(ds)
    if date in data[column].keys():
        return data[column][date]
    else:
        return None

def get_sorted_data(data):
    data_cpy = dict()
    for col in data.keys():
        data_cpy[col] = dict()
        for date in sorted(data[col].keys()):
            data_cpy[col][date] = data[col][date]

    return data_cpy