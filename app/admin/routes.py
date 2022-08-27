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

from flask import render_template, redirect, url_for, current_app, flash
from flask_login import login_required, current_user

from app import db
from app.admin import bp
import app.admin.roles as permissions

# def determine_home():
#     """determine_home [summary]

#     Returns:
#         str: Response
#     """
#     if current_app.config["MYPHP_SETUP"]:
#         return redirect(url_for("setup.index"))
#     else:
#         return redirect(url_for("main.index"))


@login_required
@permissions.view_homepage.require()
def index():
    """index 
    
    Generate a page with gives links to other apps.
    """

    kw = {
        "title" : "Admin Dashboard",
        #"username" : current_user.username
    }
    return render_template("admin/index.html", **kw)

# def flash_test():
#     flash('TEST')
#     flash('TEST info', 'info')
#     flash('TEST warning', 'warning')
#     flash('Danger', 'danger')
#     flash('message primary', 'primary')
#     flash('message secondary', 'secondary')
#     return redirect(url_for('main.index'))

