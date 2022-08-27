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

from functools import wraps
import threading

from flask import (
    redirect,
    url_for,
    flash,
    request,
    abort,
    session,
    render_template,
    current_app
)
from flask_login import current_user
from flask_mail import Message
import jwt
from werkzeug.security import check_password_hash

from app import mail
from app.models import ReloginToken

def relogin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        tokentype = session.get("_MYPHP_RELOGIN_TOKENTYPE", "jwt")
        if tokentype == "dbtoken":
            # db based token
            if "_MYPHP_RELOGIN_TOKEN" in session:
                rlt = ReloginToken.query.get(session["_MYPHP_RELOGIN_TOKEN"])
                if not rlt.check(
                            ipaddr=request.remote_addr,
                            user_agent=request.user_agent.string,
                        ):
                    flash("You have to relogin due to inactivity, change of "
                        "wifi network, or browser.")
                    session.pop("_MYPHP_RELOGIN_TOKEN")
                    # abort(400)
                    return redirect(url_for("auth.reauth", next=request.path, 
                                            tokentype='dbtoken'))
                
                # if request.method != "GET":
                #     session.pop("_MYPHP_RELOGIN_TOKEN")
                #     flash("Your Relogin token has expired.")
            else:
                return redirect(url_for("auth.reauth", next=request.path, 
                                        tokentype='dbtoken'))
        elif tokentype == "jwt":
            if "_MYPHP_RELOGIN_TOKEN" in session:
                rltk = session["_MYPHP_RELOGIN_TOKEN"]
                try:
                    rlt = jwt.decode(rltk, current_app.config['SECRET_KEY'],
                                    algorithms=['HS256'])
                except:
                    flash("You have to relogin due to inactivity.")
                    session.pop("_MYPHP_RELOGIN_TOKEN")
                    return redirect(url_for("auth.reauth", next=request.path, 
                                                tokentype='jwt'))
                else:
                    if not (rlt["ipaddr"] == request.remote_addr and
                            check_password_hash(rlt["user_agent"], request.user_agent.string)):
                        flash("You have to relogin due to change of "
                              "wifi network, or browser.")
                        session.pop("_MYPHP_RELOGIN_TOKEN")
                        return redirect(url_for("auth.reauth", next=request.path, 
                                                tokentype='jwt'))
            else:
                return redirect(url_for("auth.reauth", next=request.path, 
                                        tokentype='jwt'))
        else:
            flash('Sorry, there is an error in the application relogin '
                  'mechanism. You have been logged out for your safety.'
                  ' Please login again.', 'danger')
            return redirect(url_for("auth.logout"))

        return f(*args, **kwargs)
    return decorated_function

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    threading.Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[MyPHP] Reset Your Password',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('auth/emails/rpr.txt',
                                         user=user, token=token),
               html_body=render_template('auth/emails/rpr.html',
                                         user=user, token=token))
   

def send_new_account_email(email_id, token):
    send_email('[MyPHP] Account Creation Request',
               sender=current_app.config['ADMINS'][0],
               recipients=[email_id],
               text_body=render_template('auth/emails/newaccount.txt',
                                         email=email_id, token=token),
               html_body=render_template('auth/emails/newaccount.html',
                                         email=email_id, token=token))