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

from flask import (
    render_template,
    redirect,
    url_for,
    flash
)
from flask_login import login_required, current_user

from app import db
from app.models import User
from app.auth.helpers import relogin_required
from app.profile.forms import EditUserInfoForm
from app.profile import bp


@bp.route('/')
@login_required
def index():
    """index 
    
    Generate a page with profile info.
    """

    kw = {
        "title" : "Profile",
        #"username" : current_user.username
    }
    return render_template("profile/profile.html", **kw)


@bp.route('/logout_all_sessions', methods=['GET', 'POST'])
@login_required
@relogin_required
def logout_all_sessions():
    u = User.query.get(int(current_user.id))
    u.generate_uid()
    db.session.commit()

    flash('All devices have been logged out.')
    return redirect(url_for('profile.index'))
    # return render_template("profile/las.html", 
    #     title="Logout all sessions")


@bp.route("/edit",  methods=['GET', 'POST'])
@login_required
@relogin_required
def edit():
    u = User.query.get(int(current_user.id))

    form = EditUserInfoForm(obj=u)

    if form.validate_on_submit():
        u.email = form.email.data
        u.full_name = form.full_name.data
        db.session.commit()
        flash("Success! Profile updated.")

    return render_template("profile/edit.html", 
        title="Edit Profile",
        form=form)