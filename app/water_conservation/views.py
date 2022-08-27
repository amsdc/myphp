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
from app.models import WaterConservation
from app.water_conservation import bp
from app.water_conservation.forms import WaterSavingForm


def index():
    """determine_home [summary]

    Returns:
        str: Response
    """
    return render_template("water_conservation/index.html")


@login_required
def new_evaluation():
    if current_user.water_profile.first():
        flash("You have already filled out the form!", "danger")
        return redirect(url_for("water_conservation.index"))

    form = WaterSavingForm()
    
    if form.validate_on_submit():
        wc = WaterConservation(
            user=current_user,
            no_of_taps=form.no_of_taps.data,
            no_of_leaky_taps=form.no_of_ltaps.data,
            delta_leakage_per_min=form.t_leakrate.data,
            avg_flow_rate=form.t_flowrate.data,
            time_to_wash_vessel=form.t_dishwash.data,
            saved_using_rwh=form.s_rwh.data
        )
        wc.calculate()
        db.session.add(wc)
        db.session.commit()
        flash("Added your water conservation report successfully!")
        return redirect(url_for("water_conservation.index"))
    
    return render_template("water_conservation/new.html",
                           form=form)


def leaderboard():
    leaderlst = WaterConservation.query.order_by(WaterConservation.total_water_used.asc())

    return render_template("water_conservation/leaderboard.html", leaders=leaderlst,
                           enumerate=enumerate)
