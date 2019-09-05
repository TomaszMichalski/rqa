from datetime import timedelta

# number of addresses below which a warning is displayed
ADDRESSES_WARNING_NUM = 5
# weight of addresses in weighted average below which a warning is displayed
ADDRESSES_WARNING_WEIGHT = 0.5

PM25_WHO_NORM = 25
PM10_WHO_NORM = 50

# start date of data gathering, used as date_from in fetching past data for prediction purpose
PREDICTION_PAST_DATA_START = '2019-06-01 00:00:00'

# supported air quality columns
AIR_COLUMNS = ['pm1', 'pm25', 'pm10']
# supported weather info columns
WEATHER_COLUMNS = ['temperature', 'pressure', 'humidity', 'wind_speed', 'wind_degree', 'clouds']

COLUMNS_NAMES = {
    'pm1': 'PM1',
    'pm25': 'PM2.5',
    'pm10': 'PM10',
    'temperature': 'Temperature',
    'pressure': 'Pressure',
    'humidity': 'Humidity',
    'wind_speed': 'Wind speed',
    'wind_degree': 'Wind degree',
    'clouds': 'Clouds'
}

# timedelta of data points
DATA_TIMEDELTA = timedelta(hours=6)

# date format
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

# guest information about registered user functionalities
GUEST_MESSAGE = "Please note that this is a demo version of RQA app.\nBy registering, you gain plenty of functionalities - analysis and prediction based on your preferences, custom examinations, configuration options, groups, and more!"

STATISTIC_DATA_DEC_PLACES = 3

ANALYSIS_POINTS_NUM_MESSAGE = 'Analysis based on {} point(s) in given area.'
ANALYSIS_INACCURATE_POINTS_NUM_LOW_WARNING = 'Analysis may be inaccurate due to low point number in area.'
ANALYSIS_INACCURATE_POINTS_FAR_FROM_CENTER_WARNING = 'Analysis may be inaccurate due to points being far from area center.'

PREDICTION_POINTS_NUM_MESSAGE = 'Prediction based on {} point(s) in given area.'
PREDICTION_INACCURATE_POINTS_NUM_LOW_WARNING = 'Prediction may be inaccurate due to low point number in area.'
PREDICTION_INACCURATE_POINTS_FAR_FROM_CENTER_WARNING = 'Prediction may be inaccurate due to points being far from area center.'

DAYS_EXCEEDING_PM25_WHO_NORM_MESSAGE = '{0} measurement(s) when PM2.5 WHO norm was exceeded.'
DAYS_EXCEEDING_PM10_WHO_NORM_MESSAGE = '{0} measurement(s) when PM10 WHO norm was exceeded.'

INVALID_DATE_FROM_MESSAGE = "Date from format is invalid, provide date in format YYYY-MM-DD HH:MM:SS"
INVALID_DATE_TO_MESSAGE = "Date to format is invalid, provide date in format YYYY-MM-DD HH:MM:SS"
RADIUS_SHOULD_BE_NUMBER = "Radius should be a number"
DATE_TO_MUST_BE_GREATER_THAN_DATE_FROM = "Date to must be greater than date from"
ADDRESS_NOT_RECOGNISED = "Address cannot be recognised"
ADDRESS_NOT_SUPPORTED = "There are no installations for given address"