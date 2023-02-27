import os

import dotenv
from celery import Celery
from flask import Flask
from flask_migrate import Migrate
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

dotenv.load_dotenv()

from config import Config

db = SQLAlchemy()
celery = Celery()
api = Api()
migrate = Migrate()


def create_app():
    app = create_base_app()
    app.jinja_env.globals["paypal_client"] = os.getenv("PAYPAL-CLIENT")

    from api.controller import api_blpr
    api.init_app(api_blpr)
    app.register_blueprint(api_blpr)

    from main.controller import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

        from api.services import init_regions
        init_regions()

    migrate.init_app(app, db)

    return app


def create_base_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    celery.conf.update(app.config["CELERY_CONFIG"])
    celery.config_from_object(app.config)

    return app
