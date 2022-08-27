from flask import jsonify

from app.api import bp

@bp.errorhandler(404)
def not_found(error):
    return jsonify({"message": "Not Found"}), 404