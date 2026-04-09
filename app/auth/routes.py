from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, logout_user, current_user
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.auth import auth_bp
from app.auth.forms import RegistrationForm, LoginForm
from app.models.user import User
from app.extensions import db
import sqlalchemy as sa
from urllib.parse import urlparse

limiter = Limiter(key_func=get_remote_address)


@auth_bp.route("/register", methods=["GET", "POST"])
@limiter.limit("5 per hour")  # Limit spam registrations
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = db.session.scalar(
            sa.select(User).filter_by(email=form.email.data)
        )
        if existing_user:
            flash("Registration process completed. Please check your email.", "info")
            return redirect(url_for("auth.login"))

        user = User(
            email=form.email.data,
            height=form.height.data,
            weight=form.weight.data,
            birth_date=form.birth_date.data,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash("Account created successfully!", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", title="Register", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
@limiter.limit("10 per minute")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).filter_by(email=form.email.data))

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            if not next_page or urlparse(next_page).netloc != "":
                next_page = url_for("main.dashboard")
            return redirect(next_page)

        flash("Login Unsuccessful. Please check credentials.", "danger")

    return render_template("auth/login.html", title="Login", form=form)
