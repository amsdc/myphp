from flask import Blueprint

# This is auth blueprint
bp = Blueprint('setup', __name__)

from app.setup import routes