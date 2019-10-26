from statistics import mean, median, stdev
from . import util
from . import consts

def get_statistics_for_data(data):
    result = dict()
    data_cpy = util.extract_factor_data(data)
    for factor, factor_data in data_cpy.items():
        result[util.get_factor_name(factor)] = get_statistics_for_factor(factor_data)

    return result

def get_statistics_for_factor(factor_data):
    result = dict()
    result['mean'] = get_mean_for_factor(factor_data)
    result['median'] = get_median_for_factor(factor_data)
    result['stdev'] = get_stdev_for_factor(factor_data)

    return result

def get_mean_for_factor(factor_data):
    try:
        return round(mean(factor_data.values()), consts.STATISTIC_DATA_DEC_PLACES)
    except:
        return 0

def get_median_for_factor(factor_data):
    try:
        return round(median(factor_data.values()), consts.STATISTIC_DATA_DEC_PLACES)
    except:
        return 0

def get_stdev_for_factor(factor_data):
    try:
        return round(stdev(factor_data.values()), consts.STATISTIC_DATA_DEC_PLACES)
    except:
        return 0

def append_statistics_info(info, data):
    info.append(consts.MEASUREMENTS_EXCEEDING_PM25_WHO_NORM_MESSAGE.format(get_measurements_exceeding_pm25_who_norm(data)))
    info.append(consts.MEASUREMENTS_EXCEEDING_PM10_WHO_NORM_MESSAGE.format(get_measurements_exceeding_pm10_who_norm(data)))

    return info

def append_prediction_statistics_info(info, data, algorithm):
    info.append(consts.MEASUREMENTS_EXCEEDING_PM25_WHO_NORM_MESSAGE_WITH_ALGORITHM.format(get_measurements_exceeding_pm25_who_norm(data), algorithm))
    info.append(consts.MEASUREMENTS_EXCEEDING_PM10_WHO_NORM_MESSAGE_WITH_ALGORITHM.format(get_measurements_exceeding_pm10_who_norm(data), algorithm))

    return info

def get_measurements_exceeding_pm25_who_norm(data):
    return len(list(filter(lambda val: val > consts.PM25_WHO_NORM, data['pm25'].values())))

def get_measurements_exceeding_pm10_who_norm(data):
    return len(list(filter(lambda val: val > consts.PM10_WHO_NORM, data['pm10'].values())))