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
    SubmitField,
    IntegerField
)
from wtforms.validators import (
    ValidationError,
    DataRequired,
    InputRequired,
    Email,
    EqualTo
)


class WaterSavingForm(FlaskForm):
    no_of_taps = IntegerField('Enter the number of taps in your house?', 
                             validators=[InputRequired()])
    no_of_ltaps = IntegerField('Enter the number of leaky taps in your house?', 
                             validators=[InputRequired()])
    t_flowrate = IntegerField('Enter the flow rate of these taps in L/min', 
                             validators=[InputRequired()])
    t_leakrate = IntegerField('Enter the leakage rate of these taps in L/min', 
                             validators=[InputRequired()])
    t_dishwash = IntegerField('Enter the time taken to wash dishes in min', 
                             validators=[InputRequired()])
    s_rwh = IntegerField('Enter the water saved using RWH im m^3', 
                             validators=[InputRequired()])
    
    submit = SubmitField('Submit')


