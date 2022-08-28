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

__version__ = "0.3.0"

from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session
from flask_login import LoginManager, current_user
from flask_xcaptcha import XCaptcha
from flask_principal import Principal, identity_loaded, RoleNeed, UserNeed
from flask_mail import Mail
from flask_bootstrap import Bootstrap

from config import Config

db = SQLAlchemy()
migrate = Migrate(compare_type=True)
# sess = Session()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please log in to access this page.'
xcaptcha = None
# added patch for xcaptcha
# xcaptcha = XCaptcha()
principals = Principal()
mail = Mail()
bootstrap = Bootstrap()


def create_app(config_class=Config):
    global xcaptcha

    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    # sess.init_app(app)
    login.init_app(app)
    xcaptcha = XCaptcha(app=app) # I don't have init_app
    # xcaptcha.init_app(app)
    principals.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        # Set the identity user object
        identity.user = current_user

        # Add the UserNeed to the identity
        if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(current_user.id))

        # Assuming the User model has a list of roles, update the
        # identity with the roles that the user provides
        # if hasattr(current_user, 'get_roles') \
        #         and callable(getattr(current_user, 'get_roles')):
        if current_user.is_authenticated:
            for role in current_user.get_roles():
                identity.provides.add(RoleNeed(role))

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.profile import bp as profile_bp
    app.register_blueprint(profile_bp, url_prefix='/profile')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    from app.user_management import bp as user_management_bp
    app.register_blueprint(user_management_bp, url_prefix='/admin/users')

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    if app.config["MYPHP_SETUP"]:
        from app.setup import bp as setup_bp
        app.register_blueprint(setup_bp, url_prefix='/setup')
    
    # Applications
    
    from app.main.helpers import applications_table
    
    @app.context_processor
    def apptable():
        return {'applications_table': applications_table}

    return app

# from app import routes
