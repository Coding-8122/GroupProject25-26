from urllib.parse import urlparse
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, logout_user, current_user
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import sqlalchemy as sa

from app.auth import auth_bp
from app.auth.forms import RegistrationForm, LoginForm
from app.models.user import User
from app.extensions import db

# Initialize Limiter for auth routes
limiter = Limiter(key_func=get_remote_address)

@auth_bp.route('/register', methods=['GET', 'POST'])
@limiter.limit("5 per hour")
def register():
    """Handles new user registration with rate limiting."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = RegistrationForm()
    if form.validate_on_submit():
        # Security: Prevent account enumeration
        existing_user = db.session.scalar(sa.select(User).filter_by(email=form.email.data))
        if existing_user:
            flash('If this email is registered, you will receive a notification.', 'info')
            return redirect(url_for('auth.login'))

        user = User(
            email=form.email.data,
            height=form.height.data,
            weight=form.weight.data,
            birth_date=form.birth_date.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', title='Register', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
def login():
    """Handles user authentication with brute-force protection."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).filter_by(email=form.email.data))

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)

            # Security: Prevent Open Redirect attacks
            next_page = request.args.get('next')
            if not next_page or urlparse(next_page).netloc != '':
                next_page = url_for('main.dashboard')

            return redirect(next_page)
        else:
            flash('Login Unsuccessful. Please check email and password.', 'danger')

    return render_template('auth/login.html', title='Login', form=form)


@auth_bp.route('/logout')
def logout():
    """Terminates the user session."""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))