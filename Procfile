web: gunicorn rqa.wsgi
clock: python ./dbservice/scheduler.py
worker: celery worker --app=tasks.app