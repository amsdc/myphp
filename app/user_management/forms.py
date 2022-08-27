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

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SelectField,
    SubmitField
)
from wtforms.validators import (
    ValidationError,
    DataRequired,
    Email,
    EqualTo
)

from app.models import User

class UserRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(),
                                           EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class EditUserProfileForm(FlaskForm):
    #:str: The name of user
    full_name = StringField('Full Name', validators=[DataRequired()])
    #:str: Username
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update Profile')


class ChangePasswordForm(FlaskForm):
    # opassword = PasswordField('Old Password', validators=[DataRequired()])
    password = PasswordField('New Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(),
                                           EqualTo('password')])
    submit = SubmitField('Reset Password')


class DeleteUserForm(FlaskForm):
    confirmation = StringField("Type 'I am sure' here to proceed without the quotes",
         validators=[DataRequired()])
    submit = SubmitField('Delete User')

class AddRoleForm(FlaskForm):
    # opassword = PasswordField('Old Password', validators=[DataRequired()])
    # category = SelectField('Category',
        # choices=[
            # ("user.profile","User Profile"),
            # ("user.preferences","User Preferences"),
            # ("user_management","User Control Panel")
            # ],
        # validators=[DataRequired()])
    category = StringField("Category", validators=[DataRequired()])
    scope = StringField("Scope", validators=[DataRequired()])
    submit = SubmitField("Add role")