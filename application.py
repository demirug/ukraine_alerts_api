import dotenv
from flask import Flask

from config import Config

dotenv.load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

from controllers import *