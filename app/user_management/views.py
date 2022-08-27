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

import json
import urllib.parse

from flask import (
    render_template,
    redirect,
    request,
    url_for,
    flash,
    abort,
    current_app,
    session
)
from flask_login import (
    login_required, 
    current_user,
    logout_user,
    login_user
)
from flask_principal import (
    Identity, AnonymousIdentity, identity_changed
)

from app import db
from app import xcaptcha
from app.models import User, Role
from app.auth.helpers import relogin_required
# from app.user_management import bp
import app.user_management.roles as permissions
from app.user_management.forms import (
    EditUserProfileForm,
    ChangePasswordForm,
    AddRoleForm,
    UserRegistrationForm
)
from app.user_management import helpers

@login_required
@relogin_required
def confirmation_page():
    if not( "action" in request.args
           and "data" in request.args):
        abort(400)
    action = request.args["action"]
    data = urllib.parse.unquote(request.args["data"])
    msg = helpers.MESSAGE_MAPPING.get(action, "Are you sure you want to"
                                              " do this?")
    
    if "_confirmation" in request.args:
        return redirect(url_for(helpers.ACTION_MAPPING[action],
                       **json.loads(data)))
        
    return render_template("user_management/_confirmation.html",
                           confirm_uri=url_for("user_management.confirmation_page", 
                                               _confirmation="1", **request.args),
                           message=msg)


@login_required
@relogin_required
@permissions.add_users.require()
def add_user():
    # if current_user.is_authenticated:
    #     return redirect(url_for('main.index'))

    form = UserRegistrationForm()
    if form.validate_on_submit():
        if xcaptcha.verify():
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            user.generate_uid()
            user.suspend()
            db.session.add(user)
            db.session.commit()
            flash('Added user! Please activate the user.')
            # return redirect(url_for('auth.login'))
        else:
            flash("Error: Captcha invalid")
    return render_template('user_management/add.html', title='Register',
                           form=form)


#http_exception=403
# @bp.route("/")
@login_required
@relogin_required
@permissions.list_users.require()
def list_():
    all_users = User.query.all()

    return render_template(
            "user_management/list.html",
            title="All users",
            users=all_users,
            urlencode=urllib.parse.quote, 
            jsonify=json.dumps
        )


# @bp.route("/<int:id>/profile", methods=['GET', 'POST'])
@login_required
@relogin_required
@permissions.view_profile.require()
def profile(id):
    user = User.query.filter_by(id=id).first_or_404()
    # if user.id == current_user.id or user.id == 1:
    if user.id == current_user.id:
        abort(400)
    else:
        return render_template(
                "user_management/profile.html",
                title=f"{user.get_name()}'s profile",
                user=user,
                urlencode=urllib.parse.quote, 
                jsonify=json.dumps
            )

# @bp.route('/<int:id>/logout_all_sessions', methods=['GET', 'POST'])
@login_required
@relogin_required
@permissions.logout_user.require()
def logout_all_sessions(id):
    u = User.query.get(id)

    if u.id == current_user.id:
        abort(400)

    u.generate_uid()
    db.session.commit()

    flash('All devices of this user have been logged out.')
    return redirect(url_for('user_management.profile', id=id))


# @bp.route("/<int:id>/edit_profile", methods=["GET", "POST"])
@login_required
@relogin_required
@permissions.edit_profile.require()
def edit_profile(id):
    u = User.query.get(int(id))

    if u.id == current_user.id:
        abort(400)

    form = EditUserProfileForm(obj=u)

    if form.validate_on_submit():
        u.email = form.email.data
        u.full_name = form.full_name.data
        db.session.commit()
        flash("Success! Profile updated.")
        return redirect(url_for('user_management.profile', id=id))

    return render_template("profile/edit.html", 
        title="Edit Profile",
        form=form)


@login_required
@relogin_required
@permissions.change_user_pwd.require()
def change_password(id):
    form = ChangePasswordForm()

    u = User.query.get(int(id))

    if u.id == current_user.id:
        abort(400)

    if request.method == 'POST':
        # If request is HTTP Post, check form
        captcha_check = xcaptcha.verify()
        if captcha_check and form.validate_on_submit():
            # Verified captcha
            u.set_password(form.password.data)
            db.session.commit()
            flash("Password reset for user succeded.")
            return redirect(url_for('user_management.logout_all_sessions', id=id))
        else:
            if not captcha_check:
                flash("CAPTCHA is incorrect!")
            else:
                flash("Correct the below errors!")
    
    return render_template('user_management/changepwd.html', form=form, user=u)


@login_required
@relogin_required
@permissions.suspend_user.require()
def suspend_user(id):
    u = User.query.get(id)

    if u.id == current_user.id or u.is_suspended():
        abort(400)

    u.suspend()
    db.session.commit()
    flash("User suspended")
    return redirect(url_for('user_management.logout_all_sessions', id=id))


@login_required
@relogin_required
@permissions.activate_user.require()
def activate_user(id):
    u = User.query.get(id)

    if u.id == current_user.id:
        abort(400)

    u.activate()
    db.session.commit()
    flash("User activated")
    return redirect(url_for('user_management.profile', id=id))


@login_required
@relogin_required
@permissions.delete_user.require()
def delete_user(id):
    u = User.query.get(id)

    if u.id == current_user.id or not u.is_suspended():
        abort(400)

    db.session.delete(u)
    db.session.commit()
    flash("User is gone!")
    return redirect(url_for('user_management.list_'))


@login_required
@relogin_required
@permissions.impersonate_user.require()
def impersonate_user(id):
    u = User.query.get(id)

    if u.id == current_user.id or not u.is_suspended():
        abort(400)

    logout_user()

    # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    # Tell Flask-Principal the user is anonymous
    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())
    
    # Login the user
    login_user(u, remember=False)
    # Tell Flask-Principal the identity changed
    identity_changed.send(current_app._get_current_object(),
                          identity=Identity(u.id))
                          
    flash("You are impersonating "+u.get_name())
    
    return redirect(url_for('main.index'))


@login_required
@relogin_required
@permissions.list_roles.require()
def list_roles(id: int) -> str:
    """list_roles 
    
    List the roles of a given user

    Args:
        id (int): The ID of the user

    Returns:
        str: The HTML template.
    """
    user = User.query.filter_by(id=id).first_or_404()
    return render_template(
            "user_management/roles/list.html",
            title="Roles for {}".format(user.get_name()),
            user=user, urlencode=urllib.parse.quote, 
            jsonify=json.dumps)

@login_required
@relogin_required
@permissions.add_roles.require()
def add_roles(id: int) -> str:
    """add_roles 
    
    Add the roles of a given user

    Args:
        id (int): The ID of the user

    Returns:
        str: The HTML template.
    """
    user = User.query.filter_by(id=id).first_or_404()
    form = AddRoleForm()
    if form.validate_on_submit():
        r = Role(
            category=form.category.data,
            scope=form.scope.data,
            user=user
        )
        db.session.add(r)
        db.session.commit()
        flash("Success")
        return redirect(url_for("user_management.list_roles", id=id))
    
    return render_template(
            "user_management/roles/add.html",
            title="Role add for {}".format(user.get_name()),
            user=user, form=form)

@login_required
@relogin_required
@permissions.edit_roles.require()
def edit_role(user_id:int, role_id: int) -> str:
    """edit_role 
    
    Edit role for role_id

    Args:
        role_id (int): ID of role

    Returns:
        str: html
    """
    role = Role.query.filter_by(id=role_id).first_or_404()
    if role.user.id != user_id:
        abort(400)
    user = role.user
    form = AddRoleForm(obj=role)
    if form.validate_on_submit():
        role.category=form.category.data
        role.scope=form.scope.data

        db.session.commit()
        flash("Success", "success")
        return redirect(url_for("user_management.list_roles", id=user_id))
    
    return render_template(
            "user_management/roles/add.html",
            title="Role edit for {}".format(user.get_name()),
            user=user, form=form)

@login_required
@relogin_required
@permissions.delete_roles.require()
def delete_role(user_id:int, role_id: int) -> str:
    """delete_role 
    
    delete role for role_id

    Args:
        role_id (int): ID of role

    Returns:
        str: html
    """
    role = Role.query.filter_by(id=role_id).first_or_404()
    if role.user.id != user_id:
        abort(400)

    db.session.delete(role)
    db.session.commit()
    flash("The role has been deleted!", "success")
    return redirect(url_for("user_management.list_roles", id=user_id))
