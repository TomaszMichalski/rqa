import celery
import os
import json
from . import db
from . import statistics

app = celery.Celery('RQA')

app.conf.update(BROKER_URL=os.environ['REDIS_URL'], CELERY_RESULT_BACKEND=os.environ['REDIS_URL'])

@app.task
def get_analysis_data_async(parameters):
    data = db.get_analysis_data(parameters)
    info = data['info']
    info = statistics.append_statistics_info(info, data)
    stats = statistics.get_statistics_for_data(data)
    data = json.dumps(data)

    return return data, info, stats

@app.task
def get_prediction_data_async(parameters):
    data = db.get_prediction_data(parameters)
    info = data['info']
    info = statistics.append_statistics_info(info, data)
    stats = statistics.get_statistics_for_data(data)
    data = json.dumps(data)

    return return data, info, stats