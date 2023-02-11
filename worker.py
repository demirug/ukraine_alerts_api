import os
import re
from importlib.machinery import SourceFileLoader

from celery import Celery

from application import create_base_app


def __import_tasks(directory=os.getcwd()):
    """ Recursion searching and importing py files with name tasks.py or task_{any_name}.py """
    for file in os.listdir(directory):
        path = os.path.join(directory, file)
        if os.path.isdir(path):
            __import_tasks(path)
        if re.match("^((tasks)|(task_[aA-zZ0-9_]+)).py$", file):
            # Remove .py extension in registration name
            SourceFileLoader(file[:-3], path).load_module()


def make_celery(app):
    celery = Celery(app.import_name)

    celery.conf.update(app.config["CELERY_CONFIG"])

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    __import_tasks()
    return celery


flask_app = create_base_app()
celery = make_celery(flask_app)
