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
    SubmitField
)
from wtforms.validators import (
    ValidationError,
    DataRequired,
    Email,
    EqualTo
)

from app.models import User


class EditUserInfoForm(FlaskForm):
    #:str: The name of user
    full_name = StringField('Full Name', validators=[DataRequired()])
    #:str: Username
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update Information')