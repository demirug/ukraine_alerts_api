import dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import Config

dotenv.load_dotenv()

db = SQLAlchemy()

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

from models import *

with app.app_context():
    db.create_all()

from routes import *