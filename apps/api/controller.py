from flask import Blueprint

api_blpr = Blueprint('api', __name__, url_prefix='/api', template_folder='templates', static_folder='static')

from .models import *
from .routes import *
from .cli import *