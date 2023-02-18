import os
from datetime import timedelta


class Config:
    DEBUG = os.getenv("DEBUG")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///flask.db'

    REDIS_HOST = os.getenv("REDIS_HOST")
    REDIS_PORT = os.getenv("REDIS_PORT")

    CELERY_CONFIG = {
        'broker_url': f'redis://{REDIS_HOST}:{REDIS_PORT}/0',
        'result_backend': f'redis://{REDIS_HOST}:{REDIS_PORT}/0',
        'accept_content': ['application/json'],
        'task_serializer': 'json',
        'result_serializer': 'json',

        'beat_schedule': {
            'update_alert_info': {
                'task': 'tasks.update_status_selenium',
                'schedule': timedelta(seconds=30)
            }
        }
    }

