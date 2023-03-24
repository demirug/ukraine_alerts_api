import os
from datetime import timedelta


class Config:
    DEBUG = os.getenv("DEBUG")
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///flask.db'

    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_URL = os.getenv("REDIS_URL")
    CACHE_DEFAULT_TIMEOUT = 300

    # Price for registering callback client in USD
    CALLBACK_REGISTER_PRICE = 1
    RENDER_ALERT_MAP = False

    CELERY_CONFIG = {
        'broker_url': os.getenv("REDIS_URL"),
        'result_backend': os.getenv("REDIS_URL"),
        'accept_content': ['application/json'],
        'task_serializer': 'json',
        'result_serializer': 'json',

        'beat_schedule': {
            'update_alerts_in_ua_selenium': {
                'task': 'tasks.update_status_alerts_in_ua_selenium',
                'schedule': timedelta(minutes=15)
            },

            'update_alerts_com_ua_API': {
                'task': 'tasks.update_status_alerts_com_ua_API',
                'schedule': timedelta(seconds=5)
            },

            'update_ukrainealarm_com_API': {
                'task': 'tasks.update_status_ukrainealarm_com_API',
                'schedule': timedelta(seconds=5)
            },

            'update_vadimklimenko_statuses': {
                'task': 'tasks.update_status_vadimklimenko_statuses',
                'schedule': timedelta(seconds=5)
            }
        }
    }
