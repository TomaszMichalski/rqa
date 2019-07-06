from . import consts
from . import db

def predict(past_data, date_from, date_to):
    # create empty prediction data object
    data = db.empty_data()

    # calculate prediction data
    # TODO PLACEHOLDER
    data = calculate_placeholder_prediction_data(past_data, date_from, date_to)

    return data

def calculate_placeholder_prediction_data(past_data, date_from, date_to)
    def past_data_delta = date_from - consts.PREDICTION_PAST_DATA_START

    # iterate over columns
    # for every date in past data for the current column, fill date + i * past_data_delta with the same value
    # where i is the number of iteration
    # to this while calculated date < date_to
    # sufficient for a placeholder
    # maybe do some data revert

    return db.empty_data()