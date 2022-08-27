from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    IntegerField,
    SelectField
)
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
# from flask_babel import _, lazy_gettext as _l
from app.models import User


class DBInfoForm(FlaskForm):
    db_username = StringField('Database Username', validators=[DataRequired()])
    db_password = PasswordField('Database Password', validators=[DataRequired()])
    db_port = IntegerField('Database Port', validators=[DataRequired()], default=3306)
    # remember_me = BooleanField('Remember Me')
    db_name = StringField('Database Name', validators=[DataRequired()])
    
    c_choice = SelectField(
            'Choose a CAPTCHA',
            choices=[
                ('h', 'HCaptcha (reccomended)'), 
                ('gre', 'Google ReCaptcha'), 
                ],
            validators=[DataRequired()]
        )

    c_sitekey = StringField('Site Key', validators=[DataRequired()])
    c_secret = StringField('Secret Key', validators=[DataRequired()])
    
    submit = SubmitField('Update Configuration')

    def validate_db_username(self, username):
        if username.data.lower() == "root":
            raise ValidationError('Root users are not allowed, create '
                                  'another user with privilleges for '
                                  'only the required database.')


class CreateDBForm(FlaskForm):
    vtext = StringField('Type Proceed below', validators=[DataRequired()])
    submit = SubmitField('Create Tables')

    def validate_vtext(self, vtext):
        if vtext.data.strip() != "Proceed":
            raise ValidationError('Type Proceed with capital P')