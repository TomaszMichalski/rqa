import celery
import os
from . import db

app = celery.Celery('RQA')

app.conf.update(BROKER_URL=os.environ['REDIS_URL'], CELERY_RESULT_BACKEND=os.environ['REDIS_URL'])

@app.task
def get_analysis_data_async(parameters):
    return db.get_analysis_data(parameters)

@app.task
def get_prediction_data_async(parameters):
    return db.get_prediction_data(parameters)