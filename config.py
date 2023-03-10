import os
from datetime import timedelta


class Config:
    DEBUG = os.getenv("DEBUG")
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///flask.db'

    REDIS_HOST = os.getenv("REDIS_HOST")
    REDIS_PORT = os.getenv("REDIS_PORT")

    # Price for registering callback client in USD
    CALLBACK_REGISTER_PRICE = 1

    CELERY_CONFIG = {
        'broker_url': os.getenv("REDIS_URL"),
        'result_backend': os.getenv("REDIS_URL"),
        'accept_content': ['application/json'],
        'task_serializer': 'json',
        'result_serializer': 'json',

        'beat_schedule': {
            'update_alert_info_selenium': {
                'task': 'tasks.update_status_selenium',
                'schedule': timedelta(minutes=15)
            },

            'update_alert_info_api': {
                'task': 'tasks.update_status_api',
                'schedule': timedelta(seconds=5)
            },

            'update_alert_info_mirror': {
                'task': 'tasks.update_data_mirror',
                'schedule': timedelta(seconds=5)
            }
        }
    }
