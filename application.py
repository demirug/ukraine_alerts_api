import dotenv
from celery import Celery
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

dotenv.load_dotenv()

from config import Config

db = SQLAlchemy()
celery = Celery()

def create_app():
    app = create_base_app()

    from app.controller import main
    app.register_blueprint(main, url_prefix="")

    with app.app_context():
        db.create_all()

    return app


def create_base_app():
    global app
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    celery.conf.update(app.config["CELERY_CONFIG"])
    celery.config_from_object(app.config)

    return app
