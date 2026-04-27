import time
from urllib.parse import urlparse
from flask import render_template, url_for, flash, redirect, request, current_app
from flask_login import login_user, logout_user, current_user, login_required
import sqlalchemy as sa
from app.auth import auth_bp
from app.auth.forms import RegistrationForm, LoginForm
from app.models.user import User
from app.extensions import db
from app import limiter, security_log

# ── Constant-time login delay ───────────────────────────────
# Prevents timing-based account enumeration by ensuring the login
# endpoint always takes at least this long (seconds).
_LOGIN_MIN_DELAY = 0.3


@auth_bp.route('/register', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def register():
    """Handles new user registration."""
    # Prevent logged-in users from accessing the register page
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data.lower().strip(),
            height=form.height.data,
            weight=form.weight.data,
            birth_date=form.birth_date.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        security_log.info('New account created: email=%s ip=%s',
                          user.email, request.remote_addr)
        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', title='Register', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
def login():
    """Handles user authentication and session creation."""
    # Prevent logged-in users from accessing the login page
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        start = time.monotonic()

        # Modern SQLAlchemy 2.0 query syntax
        user = db.session.scalar(
            sa.select(User).filter_by(email=form.email.data.lower().strip())
        )

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)

            security_log.info('Successful login: email=%s ip=%s',
                              user.email, request.remote_addr)

            # Secure the 'next' redirect against Open Redirect Vulnerabilities
            next_page = request.args.get('next')
            if not next_page or urlparse(next_page).netloc != '':
                next_page = url_for('main.dashboard')

            # Enforce minimum delay to prevent timing attacks
            elapsed = time.monotonic() - start
            if elapsed < _LOGIN_MIN_DELAY:
                time.sleep(_LOGIN_MIN_DELAY - elapsed)

            return redirect(next_page)
        else:
            security_log.warning(
                'Failed login attempt: email=%s ip=%s',
                form.email.data, request.remote_addr,
            )
            # Enforce minimum delay to prevent timing attacks
            elapsed = time.monotonic() - start
            if elapsed < _LOGIN_MIN_DELAY:
                time.sleep(_LOGIN_MIN_DELAY - elapsed)
            # Generic message prevents account enumeration
            flash('Login unsuccessful. Please check your credentials.', 'danger')

    return render_template('auth/login.html', title='Login', form=form)


@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """Terminates the user session. POST-only to prevent CSRF logout attacks."""
    security_log.info('User logged out: ip=%s', request.remote_addr)
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))