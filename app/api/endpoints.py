from flask import request
from flask import abort
from flask_restful import (
    Resource,  
    reqparse
)

from app import db
from app.api.auth import basic_auth, generate_token, token_auth


class Login(Resource):
    decorators = [basic_auth.login_required]
    def get(self):
        user = basic_auth.current_user()
        return {
            "token": user.generate_token()
        }


class ActiveUser(Resource):
    decorators = [token_auth.login_required]
    def get(self):
        user = token_auth.current_user()
        return {
            "id": user.id,
            "uid": user.unique_id,
            "username": user.username,
            "name": user.full_name,
            "display_name": user.get_name(),
            "email": user.email
        }


class LogoutUser(Resource):
    decorators = [token_auth.login_required]
    def get(self):
        user = token_auth.current_user()
        user.generate_uid()
        db.session.commit()
        return {
                "message": "OK"
            }
