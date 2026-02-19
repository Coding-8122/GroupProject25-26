from flask import render_template, url_for, flash, redirect, request
from flask_login import login_required, current_user
from app.extensions import db
from app.user import user_bp
from app.user.forms import UpdateProfileForm


@user_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()

    if form.validate_on_submit():
        # Update user data from form
        current_user.gender = form.gender.data
        current_user.birth_date = form.birth_date.data
        current_user.height = form.height.data
        current_user.weight = form.weight.data

        db.session.commit()
        flash('Your profile has been updated successfully!', 'success')
        return redirect(url_for('user.profile'))

    elif request.method == 'GET':
        # Pre-populate form with existing data
        form.gender.data = current_user.gender
        form.birth_date.data = current_user.birth_date
        form.height.data = current_user.height
        form.weight.data = current_user.weight

    return render_template('user/profile.html', title='My Profile', form=form)
