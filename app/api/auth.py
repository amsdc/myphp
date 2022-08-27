from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from werkzeug.security import check_password_hash
from flask import abort, current_app
import jwt
import time

# from app import mysql
from app.models import User

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()

@basic_auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user

@basic_auth.error_handler
def basic_auth_error(status):
    abort(403, "Invalid username or password")

def generate_token(uid):
    return jwt.encode({'uid': uid,
                'exp': time.time() + 6000},
    current_app.config['SECRET_KEY'], algorithm='HS256')


@token_auth.verify_token
def verify_token(token):
    try:
        jtkn = jwt.decode(token, current_app.config['SECRET_KEY'],
        algorithms=['HS256'])
        # print(jtkn)
        return User.query.filter_by(unique_id=jtkn["uid"]).first()
    except:
        return None
        

@token_auth.error_handler
def token_auth_error(status):
    abort(401, "You have not supplied a token in the headers or"
               " the token issued by your client is invalid.")