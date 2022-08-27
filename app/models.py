# This file is part of MyPHP.

# MyPHP is free software: you can redistribute it and/or modify it under 
# the terms of the GNU General Public License as published by the Free 
# Software Foundation, either version 3 of the License, or (at your 
# option) any later version.

# MyPHP is distributed in the hope that it will be useful, but WITHOUT 
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License 
# for more details.

# You should have received a copy of the GNU General Public License along
# with MyPHP. If not, see <https://www.gnu.org/licenses/>. 

import typing as t
import secrets
import string
import time
from datetime import timedelta
from datetime import datetime
from hashlib import md5

from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

from app import db, login

class User(UserMixin, db.Model):
    #:int: Integer ID
    id = db.Column(db.Integer, primary_key=True)
    #:str: Unique ID to prevent relogin on pwdreset
    unique_id = db.Column(db.String(32), index=True, unique=True)
    #:str: The name of user
    full_name = db.Column(db.String(128))
    #:str: Username
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    relogin_tokens = db.relationship('ReloginToken', backref='user', lazy='dynamic', cascade="all, delete, delete-orphan")
    roles = db.relationship('Role', backref='user', lazy='dynamic', cascade="all, delete, delete-orphan")
    
    def __repr__(self):
        return '<User {}>'.format(self.username)

    def get_id(self) -> str:
        """get_id 
        
        Get ID for Flask-Login

        Returns:
            str: UniqueID
        """
        return self.unique_id
    
    def generate_token(self):
        return jwt.encode({'uid': self.unique_id,
                'exp': time.time() + 6000},
                current_app.config['SECRET_KEY'], algorithm='HS256')

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def change_password(self, old_password: str, new_password: str) -> bool:
        """change_password 
        
        Changes the user's password, given the old one, and the new
        one. The password is changed iff the old one matches.

        Args:
            old_password (str): The previous password of the user.
            new_password (str): The new password of the user.

        Returns:
            bool: If the operation succeded or not.
        """
        if self.check_password(old_password):
            self.set_password(new_password)
            return True
        else:
            return False

    def generate_uid(self) -> None:
        """generate_uid 
        
        Generate or regenerate a UID for a user.
        """
        self.unique_id = ''.join(secrets.choice(string.ascii_letters 
            + string.digits) for i in range(32))

    def avatar(self, size):
        if self.email:
            digest = md5(self.email.lower().encode('utf-8')).hexdigest()
            return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
                digest, size)
        else:
            return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
                "default", size)

    def get_name(self):
        if self.full_name:
            return self.full_name.split()[0]
        else:
            return self.username

    def get_roles(self) -> list[str]:
        """get_roles 
        
        Get all roles of current user

        Returns:
            list of str: List of roles
        """
        roles = self.roles
        list_of_str = list()
        for role in roles:
            list_of_str.append("{}:{}".format(
                role.category, role.scope))

        return list_of_str
    
    def can_do(self, category: str, scope:str="view") -> bool:
        """can_do 
        
        Whether user has a role.

        Args:
            category (str): Category
            scope (str, optional): Scope. Defaults to "view".

        Returns:
            bool: True when role exists else False
        """
        roleobj = self.roles.filter_by(category=category, 
                                       scope=scope).first()
        
        return bool(roleobj)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.unique_id, 'exp': time.time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            unique_id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.filter_by(unique_id=unique_id).first()
    
    def is_suspended(self):
        return self.username.startswith("__")
        
    def suspend(self):
        self.username = "__" + self.username
        
    def activate(self):
        if self.is_suspended():
            self.username = self.username[2:]


@login.user_loader
def load_user(unique_id):
    """load_user 
    
    This function returns a unique string to identify users.

    Args:
        uid (str): The uniqe identifier

    Returns:
        User: User object
    """
    # return User.query.get(int(id))
    return User.query.filter_by(unique_id=unique_id).first()


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    scope = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class ReloginToken(db.Model):
    token = db.Column(db.String(64), primary_key=True)
    ipaddr = db.Column(db.String(10))
    user_agent = db.Column(db.String(200))
    created_on = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, *a, **kw) -> None:
        super().__init__(*a, **kw)
        self.generate_token()

    def generate_token(self) -> None:
        """generate_token
        
        Generate a token for a user.
        """
        self.token = ''.join(secrets.choice(string.ascii_letters 
            + string.digits) for i in range(32))

    def check(self, ipaddr: str, user_agent: str) -> bool:
        validity = (datetime.utcnow() - self.created_on) <= timedelta(minutes=30)
        # breakpoint()
        if self.ipaddr == ipaddr \
                and self.user_agent == user_agent and validity:
            return True
        else:
            return False
