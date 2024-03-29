import os

import dotenv
from celery import Celery
from flask import Flask
from flask_caching import Cache
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from swagger_ui import api_doc

dotenv.load_dotenv()

from config import Config

db = SQLAlchemy()
celery = Celery()
migrate = Migrate()
cors = CORS()
cache = Cache()


def create_app():
    app = create_base_app()
    app.jinja_env.globals["paypal_client"] = os.getenv("PAYPAL-CLIENT")

    api_doc(app, config_path='apps/api/config/swagger.yaml', url_prefix='/api', title="Ukraine Air Raid Alert API", parameters={
        "deepLinking": "false",
        "displayRequestDuration": "false",
        "layout": "\"StandaloneLayout\"",
        "plugins": "[SwaggerUIBundle.plugins.DownloadUrl]",
        "presets": "[SwaggerUIBundle.presets.apis, SwaggerUIStandalonePreset.slice(1)]",
    })

    from apps.api.controller import api_blpr
    app.register_blueprint(api_blpr)

    from apps.main.controller import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app


def create_base_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app, resources={r"/static/*": {"origins": "*"}, "/api/*": {"origins": "*"}})
    celery.conf.update(app.config["CELERY_CONFIG"])
    celery.config_from_object(app.config)
    cache.init_app(app)
    return app
