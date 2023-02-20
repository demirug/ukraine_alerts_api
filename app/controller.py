from flask import Blueprint

main = Blueprint('main', __name__, url_prefix='/api', template_folder='templates', static_folder='static')

from .models import *
from .routes import *