from flask import render_template, url_for, flash, redirect, request
from flask_login import login_required, current_user
from app.extensions import db
from app.user import user_bp
from app.user.forms import UpdateProfileForm

@user_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """
    User profile management.
    Allows updating gender, birth date, height, and weight.
    """
    form = UpdateProfileForm()

    if form.validate_on_submit():
        # Update current user instance with form data
        current_user.gender = form.gender.data
        current_user.birth_date = form.birth_date.data
        current_user.height = form.height.data
        current_user.weight = form.weight.data

        db.session.commit()
        flash('Your profile has been updated successfully!', 'success')
        return redirect(url_for('user.profile'))

    elif request.method == 'GET':
        # Populate form fields with existing data from database
        form.gender.data = current_user.gender
        form.birth_date.data = current_user.birth_date
        form.height.data = current_user.height
        form.weight.data = current_user.weight

    return render_template('user/profile.html', title='My Profile', form=form)


@user_bp.route('/settings')
@login_required
def settings ():

    return render_template('user/settings.html')