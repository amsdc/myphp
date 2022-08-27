import secrets
from urllib.parse import quote

from flask import (
    render_template, 
    redirect, 
    url_for, 
    abort, 
    flash,
    request
)
from flask_login import login_required, logout_user, current_user, login_user

from app import db
from app import xcaptcha
from app.models import User
from app.setup import bp
from app.setup.forms import (
    DBInfoForm,
    CreateDBForm
)
from app.auth.forms import RegistrationForm

@bp.route('/')
def index():
    """index 
    
    Generate a page with gives links to other apps.
    """

    return render_template("setup/step0.html")


@bp.route('/step/<int:step>/', methods=['GET', 'POST'])
def step(step: int):
    """step [summary]

    Args:
        step (int): Step #
    """
    if step == 1:
        form = DBInfoForm()
        if form.validate_on_submit():
            secret_key = secrets.token_urlsafe(16)

            DBURI = "mysql+pymysql://{username}:{password}@{ip}:{port}/{database}"

            username = form.db_username.data
            password = quote(form.db_password.data)
            ip = 'localhost'
            port = form.db_port.data
            database = form.db_name.data

            database_uri = DBURI.format(
                    username=username,
                    password=password,
                    ip=ip,
                    port=port,
                    database=database
                )

            hcaptcha = True if form.c_choice.data == "h" else False

            captcha_site_key = form.c_sitekey.data
            captcha_secret_key = form.c_secret.data

            cfg = render_template(
                    "setup/config_templates/config.py.jinja2",
                    secret_key=secret_key,
                    database_uri=database_uri,
                    hcaptcha=hcaptcha,
                    captcha_site_key=captcha_site_key,
                    captcha_secret_key=captcha_secret_key
                )

            with open("config.py", "w") as fh:
                fh.write(cfg)

            flash("The configuration has been written. Please "
                  "restart the application.")

            return redirect(url_for("setup.step", step=2))
        return render_template("setup/step1.html", form=form)
    elif step == 2:
        form = CreateDBForm()
        if form.validate_on_submit():
            db.create_all()
            flash("Database created.")
            return redirect(url_for("setup.step", step=3))
        return render_template("setup/step2.html", form=form)
    elif step == 3:
        form = CreateDBForm()
        if form.validate_on_submit():
            u = User(username="__root", email="webmaster@myphp.py")
            u.generate_uid()
            db.session.add(u)
            db.session.commit()

            login_user(u)
            # ]W6gxWZzZ.bVkCST

            flash("Root user has been created. Please create an "
                  "account using the below form.")
            
            return redirect(url_for("setup.step", step=4))

        return render_template("setup/step3.html", form=form)
    elif step == 4:
        if current_user.is_authenticated:
            form = RegistrationForm()
            if form.validate_on_submit():
                if xcaptcha.verify():
                    user = User(username=form.username.data, email=form.email.data)
                    user.set_password(form.password.data)
                    user.generate_uid()
                    db.session.add(user)
                    db.session.commit()
                    flash('Congratulations, registered user!')
                    logout_user()
                    return redirect(url_for("setup.step", step=5))
                else:
                    flash("Error: Captcha invalid")
            return render_template("setup/step4.html", form=form)
        else:
            abort(403)
    elif step == 5:
        return render_template("setup/step5.html")
    else:
        abort(400)
