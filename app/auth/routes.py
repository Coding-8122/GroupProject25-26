from flask import render_template, url_for, flash, redirect, request
from app.auth import auth_bp
from app.auth.forms import RegistrationForm
from app.models.user import User
from app.extensions import db

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            height=form.height.data,
            weight=form.weight.data,
            birth_date=form.birth_date.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)