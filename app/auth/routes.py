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
import time

from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    request,
    abort,
    session,
    current_app
)
from werkzeug.urls import url_parse
from flask_login import (
    login_user,
    logout_user,
    current_user,
    login_required
)
from flask_principal import (
    Identity, AnonymousIdentity, identity_changed
)
import jwt
from werkzeug.security import generate_password_hash

from app import db
from app import xcaptcha
from app.auth import bp
from app.auth.forms import (
    LoginForm,
    RegistrationForm,
    ChangePasswordForm,
    ReloginForm,
    ResetPasswordRequestForm,
    ResetPasswordForm,
    RegEmailSendForm
)
from app.auth.helpers import (
    send_password_reset_email,
    send_new_account_email
)
from app.models import User, ReloginToken
# from app.auth.email import send_password_reset_email


# @bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    usr_dbquery = request.args.get("query_user", "username")
    
    form = LoginForm(query_user=usr_dbquery)

    if request.method == 'POST':
        # If request is HTTP Post, check form
        captcha_check = xcaptcha.verify()
        if captcha_check and form.validate_on_submit():
            # Verified captcha
            # If email-based login:
            if usr_dbquery == "email":
                user = User.query.filter_by(email=form.username.data).first()
            elif usr_dbquery == "uid":
                user = User.query.filter_by(unique_id=form.username.data).first()
            else:
                user = User.query.filter_by(username=form.username.data).first()
            if user is None or not user.check_password(form.password.data) or user.is_suspended():
                flash('Invalid user identifier(username/email/userid etc) or password')
                return redirect(url_for('auth.login', **request.args))

            # Login the user
            login_user(user, remember=form.remember_me.data)
            # Tell Flask-Principal the identity changed
            identity_changed.send(current_app._get_current_object(),
                                  identity=Identity(user.id))

            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('main.index')
            return redirect(next_page)
        else:
            flash("CAPTCHA is incorrect!")
    
    return render_template('auth/login.html', title='Sign In', form=form)


# @bp.route('/changepwd', methods=['GET', 'POST'])
@login_required
def changepwd():
    form = ChangePasswordForm()

    if request.method == 'POST':
        # If request is HTTP Post, check form
        captcha_check = xcaptcha.verify()
        if captcha_check and form.validate_on_submit():
            # Verified captcha
            if current_user.change_password(form.opassword.data,
                form.password.data):
                db.session.commit()
                flash("Password reset succeded. Login again.")
                return redirect(url_for("auth.logout"))
            else:
                flash("Your current password seems to be incorrect.")
        else:
            if not captcha_check:
                flash("CAPTCHA is incorrect!")
            else:
                flash("Correct the below errors!")
    
    return render_template('auth/changepwd.html', form=form)


# @bp.route('/logout')
def logout():
    logout_user()

    # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    # Tell Flask-Principal the user is anonymous
    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())
    
    return redirect(url_for('auth.login'))


# @bp.route('/register', methods=['GET', 'POST'])
# @login_required
# def register():
#     # if current_user.is_authenticated:
#     #     return redirect(url_for('main.index'))
#     msg = ""

#     form = RegistrationForm()
#     if form.validate_on_submit():
#         if xcaptcha.verify():
#             user = User(username=form.username.data, email=form.email.data)
#             user.set_password(form.password.data)
#             user.generate_uid()
#             db.session.add(user)
#             db.session.commit()
#             msg = 'Congratulations, registered user!'
#             # return redirect(url_for('auth.login'))
#         else:
#             msg = "Error: Captcha invalid"
#     return render_template('auth/register.html', title='Register',
#                            form=form, msg=msg)


def public_registration():
    form = RegEmailSendForm()
    
    if form.validate_on_submit():
        if xcaptcha.verify():
            token = jwt.encode(
                {'email': form.email.data, 'exp': time.time() + 600},
                current_app.config['SECRET_KEY'], algorithm='HS256')
            send_new_account_email(form.email.data, token)
            flash("You will recieve an e-mail. Click the link.")
        else:
            flash("Check the CAPTCHA")
    
    return render_template("auth/new_account.html", form=form)


def register(token):
    try:
        jwtdata = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])
    except:
        flash("Email invite expired. Request a new one.")
        return redirect(url_for('auth.public_registration'))
    user = User.query.filter_by(email=jwtdata["email"]).first()
    
    if user is not None:
        abort(400, "Cannot create account with that email - "
              "account already exists!")
    
    form = RegistrationForm()
    if form.validate_on_submit():
        if xcaptcha.verify():
            user = User(username=form.username.data, email=jwtdata["email"])
            user.set_password(form.password.data)
            user.generate_uid()
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, registered user!')
            return redirect(url_for('auth.login'))
        else:
            flash("Error: Captcha invalid")
    
    return render_template("auth/register2.html", email=jwtdata["email"],
                           form=form)

# @bp.route('/relogin', methods=['GET', 'POST'])
@login_required
def reauth():
    # if current_user.is_authenticated:
    #     return redirect(url_for('main.index'))
    tokentype = request.args.get("tokentype", "jwt")
    if tokentype not in ["dbtoken","jwt"]:
        abort(400)
    
    
    form = ReloginForm()

    if request.method == 'POST':
        next_page = request.args.get('next')
        # If request is HTTP Post, check form
        captcha_check = xcaptcha.verify()
        if captcha_check and form.validate_on_submit():
            if not current_user.check_password(form.password.data):
                flash('Invalid password')
                return redirect(url_for('auth.reauth', **request.args))
            else:
                if tokentype == "dbtoken":
                    rlt = ReloginToken(
                            ipaddr=request.remote_addr,
                            user_agent=request.user_agent.string,
                            user_id=current_user.id
                        )
                    db.session.add(rlt)
                    db.session.commit()

                    session["_MYPHP_RELOGIN_TOKENTYPE"] = "dbtoken"
                    session["_MYPHP_RELOGIN_TOKEN"] = rlt.token
                elif tokentype == "jwt":
                    rlt = jwt.encode(
                                    {'ipaddr': request.remote_addr, 
                                     'user_agent': 
                                         generate_password_hash(request.user_agent.string),
                                     'user_id': current_user.id,
                                     'exp': time.time() + 1800},
                        current_app.config['SECRET_KEY'], algorithm='HS256')
                    session["_MYPHP_RELOGIN_TOKENTYPE"] = "jwt"
                    session["_MYPHP_RELOGIN_TOKEN"] = rlt
                
                if not next_page or url_parse(next_page).netloc != '':
                    abort(400)
                return redirect(next_page)
        else:
            flash("CAPTCHA is incorrect!")
    
    return render_template('auth/relogin.html', form=form)


# @bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if request.method == 'POST':
        if xcaptcha.verify() and form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                send_password_reset_email(user)
            flash('Check your email for the instructions to reset your password')
            return redirect(url_for('auth.login'))
        else:
            flash('Error- please correct error and refill captcha','error')
    return render_template('auth/requestpwdreset.html',
                           title='Reset Password', form=form)


# @bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user.set_password(form.password.data)
            user.generate_uid()
            db.session.commit()
            flash('Your password has been reset.')
            return redirect(url_for('auth.login'))
        else:
            flash('Error- please correct error and refill captcha','error')
    return render_template('auth/requestpwdreset.html', form=form)