import time
from urllib.parse import urlparse
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, logout_user, current_user, login_required
from app import limiter, security_log  # Import from root app package
import sqlalchemy as sa

from app.auth import auth_bp
from app.auth.forms import RegistrationForm, LoginForm
from app.models.user import User
from app.extensions import db

_LOGIN_MIN_DELAY = 0.3


@auth_bp.route("/register", methods=["GET", "POST"])
@limiter.limit("5 per hour")
def register():
    """Handles user registration with email normalization and complexity checks."""
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = RegistrationForm()
    if form.validate_on_submit():
        email_clean = form.email.data.lower().strip()
        if db.session.scalar(sa.select(User).filter_by(email=email_clean)):
            flash(
                "If this email is registered, you will receive a notification.", "info"
            )
            return redirect(url_for("auth.login"))

        user = User(
            email=email_clean,
            height=form.height.data,
            weight=form.weight.data,
            birth_date=form.birth_date.data,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        security_log.info(f"New account created: {email_clean}")
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", title="Register", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
@limiter.limit("10 per minute")
def login():
    """Login with brute-force protection and timing delay."""
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        start_time = time.monotonic()
        email_clean = form.email.data.lower().strip()
        user = db.session.scalar(sa.select(User).filter_by(email=email_clean))

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            _enforce_delay(start_time)
            return redirect(url_for("main.dashboard"))

        _enforce_delay(start_time)
        security_log.warning(f"Failed login attempt for: {email_clean}")
        flash("Login unsuccessful.", "danger")

    return render_template("auth/login.html", title="Login", form=form)


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    """Terminates session. POST-only for CSRF protection."""
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))


def _enforce_delay(start_time):
    """Mitigates timing attacks by ensuring a minimum processing time."""
    elapsed = time.monotonic() - start_time
    if elapsed < _LOGIN_MIN_DELAY:
        time.sleep(_LOGIN_MIN_DELAY - elapsed)
