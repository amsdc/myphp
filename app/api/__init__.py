from flask import Blueprint
from flask_restful import Api

# This is auth blueprint
bp = Blueprint('api', __name__)

app_api = Api(bp)

from app.api import urls