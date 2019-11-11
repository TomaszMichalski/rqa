from . import consts
from . import db
from . import util
from datetime import datetime, timedelta
import numpy as np
from sklearn.linear_model import LinearRegression
import pandas as pd
from fbprophet import Prophet
from pyramid.arima import auto_arima

# calculates prediction data from date_from to date_to using past_data
# after the process, cuts the (< date_from) part of predicted data so that
# only datetimes between date_from and date_to are present in the result
def predict(past_data, date_from, date_to):
    past_data_quarter = get_past_data_quarter(past_data)
    past_data_month = get_past_data_month(past_data)
    past_data_week = get_past_data_week(past_data)

    if consts.ENABLE_HEAVY_COMPUTING:
        fbprophet_full = calculate_prediction_data_fbprophet(past_data, date_to)
        fbprophet_quarter = calculate_prediction_data_fbprophet(past_data_quarter, date_to)
        fbprophet_month = calculate_prediction_data_fbprophet(past_data_month, date_to)
        fbprophet_prediction = aggregate_prediction_3(fbprophet_full, fbprophet_quarter, fbprophet_month)
        fbprophet_prediction = get_sorted_data(fbprophet_prediction)

    linreg_full = calculate_prediction_data_linreg(past_data, date_to)
    linreg_quarter = calculate_prediction_data_linreg(past_data_quarter, date_to)
    linreg_month = calculate_prediction_data_linreg(past_data_month, date_to)
    linreg_week = calculate_prediction_data_linreg(past_data_week, date_to)
    linreg_prediction = aggregate_prediction_4(linreg_full, linreg_quarter, linreg_month, linreg_week)
    linreg_prediction = get_sorted_data(linreg_prediction)

    arima_prediction = calculate_prediction_data_arima(past_data_month, date_to)
    arima_prediction = get_sorted_data(arima_prediction)

    historical_data = get_historical_data(past_data, date_from)
    historical_data = get_sorted_data(historical_data)

    if consts.ENABLE_HEAVY_COMPUTING:
        return historical_data, fbprophet_prediction, linreg_prediction, arima_prediction
    
    return historical_data, linreg_prediction, arima_prediction

def aggregate_prediction_3(full, quarter, month):
    result = dict()
    for col in full.keys():
        result[col] = dict()
        for date in full[col].keys():
            aggregated_value = (consts.FULL_WEIGHT * full[col][date] + consts.QUARTER_WEIGHT * quarter[col][date] + consts.MONTH_WEIGHT * month[col][date]) / (consts.FULL_WEIGHT + consts.QUARTER_WEIGHT + consts.MONTH_WEIGHT)
            result[col][date] = aggregated_value

    return result

def aggregate_prediction_4(full, quarter, month, week):
    result = dict()
    for col in full.keys():
        result[col] = dict()
        for date in full[col].keys():
            aggregated_value = (consts.FULL_WEIGHT * full[col][date] + consts.QUARTER_WEIGHT * quarter[col][date] + consts.MONTH_WEIGHT * month[col][date] + consts.WEEK_WEIGHT * week[col][date]) / (consts.FULL_WEIGHT + consts.QUARTER_WEIGHT + consts.MONTH_WEIGHT + consts.WEEK_WEIGHT)
            result[col][date] = aggregated_value

    return result

def get_historical_data(past_data, date_from):
    result = dict()
    for col in past_data.keys():
        result[col] = dict()
        for date, value in past_data[col].items():
            if datetime.strptime(date, consts.DATE_FORMAT) >= date_from:
                result[col][date] = value

    return result

def get_past_data_quarter(past_data):
    now = datetime.now()
    quarter_ago = now - timedelta(days=90)
    result = dict()
    for col in past_data.keys():
        result[col] = dict()
        for date, value in past_data[col].items():
            if datetime.strptime(date, consts.DATE_FORMAT) > quarter_ago:
                result[col][date] = value

    return result

def get_past_data_month(past_data):
    now = datetime.now()
    month_ago = now - timedelta(days=30)
    result = dict()
    for col in past_data.keys():
        result[col] = dict()
        for date, value in past_data[col].items():
            if datetime.strptime(date, consts.DATE_FORMAT) > month_ago:
                result[col][date] = value

    return result

def get_past_data_week(past_data):
    now = datetime.now()
    week_ago = now - timedelta(days=7)
    result = dict()
    for col in past_data.keys():
        result[col] = dict()
        for date, value in past_data[col].items():
            if datetime.strptime(date, consts.DATE_FORMAT) > week_ago:
                result[col][date] = value

    return result

def filter_unrealistic_values(data):
    result = dict()
    for col in data.keys():
        result[col] = dict()
        for date, value in data[col].items():
            if value < consts.BOUNDARY_VALUES[col][0]:
                value = consts.BOUNDARY_VALUES[col][0]
            elif value > consts.BOUNDARY_VALUES[col][1]:
                value = consts.BOUNDARY_VALUES[col][1]
            result[col][date] = value

    return result

def calculate_prediction_data_arima(past_data, date_to):
    result = dict()
    for col in past_data.keys():
        if len(list(past_data[col].keys())) > 0:
            result[col] = dict()
            factor = pd.DataFrame.from_dict(past_data[col], orient='index')
            factor.index = pd.to_datetime(factor.index)
            stepwise_model = auto_arima(factor, start_p=1, start_q=1, max_p=3, max_q=3, m=12, start_P=0, seasonal=True, d=1, D=1, trace=True, error_action='ignore', suppress_warnings=True, stepwise=True)
            stepwise_model.fit(factor)
            future = stepwise_model.predict(n_periods=util.get_prediction_periods(date_to))
            future_dt = util.get_prediction_datetimes_dt(datetime.now(), date_to)
            for i in range(len(future_dt)):
                result[col][future_dt[i].strftime(consts.DATE_FORMAT)] = future[i]

    result = filter_unrealistic_values(result)

    return result

def calculate_prediction_data_linreg(past_data, date_to):
    result = dict()
    for col in past_data.keys():
        if len(list(past_data[col].keys())) > 0:
            result[col] = dict()
            x = np.array(list(map(lambda x: datetime.timestamp(datetime.strptime(x, consts.DATE_FORMAT)), list(past_data[col].keys())))).reshape((-1, 1))
            y = np.array(list(past_data[col].values()))
            model = LinearRegression().fit(x, y)
            x_pred = np.array(util.get_prediction_datetimes(list(past_data[col].keys())[-1], date_to)).reshape((-1, 1))
            y_pred = model.predict(x_pred)
            for i in range(x_pred.size):
                result[col][str(datetime.fromtimestamp(x_pred.item(i)))] = y_pred.item(i)

    result = filter_unrealistic_values(result)

    return result

def calculate_prediction_data_fbprophet(past_data, date_to):
    data = util.convert_to_past_data_with_datetimes(past_data)
    result = dict()
    for col in consts.PREDICTION_ORDER:
        if len(list(past_data[col].keys())) > 0:
            result[col] = dict()
            pd.set_option('display.max_rows', 1000)
            pd.set_option('display.max_columns', 100)
            print("Starting prediction for column {}".format(col))
            # m = Prophet(weekly_seasonality=True, daily_seasonality=True, growth='logistic')
            m = Prophet(growth = 'logistic')
            df = pd.DataFrame(list(data[col].items()), columns=['ds', 'y'])
            # df = merge_regressors(df, get_pre_predicted_regressors_df(data, col))
            df = add_regressors_data(df, data, col)
            df = df.interpolate(method='linear', limit_direction='both')
            print("DF")
            print(df)
            df = apply_cap_floor(df, col)
            m = add_regressors(m, col)
            m.fit(df)
            future = m.make_future_dataframe(periods=util.get_prediction_periods(date_to), freq='6H')
            future = add_regressors_data(future, data, col)
            future = future.interpolate(method='linear', limit_direction='both')
            print("FUTURE")
            print(future)
            future = apply_cap_floor(future, col)
            forecast = m.predict(future)
            now = datetime.now()
            for index, row in forecast.iterrows():
                if row['ds'] >= now:
                    result[col][row['ds']] = row['yhat']
            print("Finished prediction for column {}".format(col))

    result = util.convert_to_past_data_with_strings(result)
    result = filter_unrealistic_values(result)

    return result

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