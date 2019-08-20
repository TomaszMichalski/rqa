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

# timedelta of data points
DATA_TIMEDELTA = timedelta(hours=6)

# date format
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

# guest information about registered user functionalities
GUEST_MESSAGE = "Please note that this is a demo version of RQA app.\nBy registering, you gain plenty of functionalities - analysis and prediction based on your preferences, custom examinations, configuration options, groups, and more!"