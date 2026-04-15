from flask import render_template, url_for, flash, redirect, request, Response
from flask_login import login_required, current_user
from sqlalchemy import func
from app.main import main_bp
from app.extensions import db
from app.models.recovery import RecoveryLog
from app.models.workout import WorkoutLog
from app.models.body_metric import BodyMetric
# Added EditProfileForm to the import list below
from app.main.forms import RecoveryLogForm, WorkoutLogForm, BodyMetricsForm, EditProfileForm
from datetime import datetime, timezone
from app.utils.recovery_calculations import calculate_recovery_hours
from app.utils.export_utils import generate_workout_csv


@main_bp.route('/', methods=['GET', 'POST'])
@main_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    """Handles recovery display and logging based on accurate daily maximum intensity."""
    form = RecoveryLogForm()
    today = datetime.now(timezone.utc).date()

    last_workout = WorkoutLog.query.filter_by(user_id=current_user.id) \
        .order_by(WorkoutLog.date.desc(), WorkoutLog.id.desc()).first()

    if form.validate_on_submit():
        log = RecoveryLog.query.filter_by(user_id=current_user.id, date=today).first()
        if not log:
            log = RecoveryLog(user_id=current_user.id, date=today)
            db.session.add(log)

        log.sleep_hours = form.sleep_hours.data
        log.muscle_soreness = form.muscle_soreness.data
        log.energy_level = form.energy_level.data
        log.stress_level = form.stress_level.data

        max_intensity = db.session.query(func.max(WorkoutLog.intensity)) \
            .filter(WorkoutLog.user_id == current_user.id, WorkoutLog.date == today).scalar()

        current_intensity = max_intensity if max_intensity else 5

        log.recovery_estimated = calculate_recovery_hours(
            intensity=current_intensity,
            soreness=log.muscle_soreness,
            sleep_hours=log.sleep_hours
        )

        db.session.commit()
        flash('Recovery metrics updated successfully.', 'success')
        return redirect(url_for('main.dashboard'))

    recent_logs = RecoveryLog.query.filter_by(user_id=current_user.id) \
        .order_by(RecoveryLog.date.desc()).limit(7).all()

    return render_template('main/dashboard.html',
                           form=form,
                           logs=recent_logs,
                           last_workout=last_workout)


@main_bp.route('/metrics', methods=['GET', 'POST'])
@login_required
def metrics():
    """Handles body weight and fat percentage tracking."""
    form = BodyMetricsForm()
    if form.validate_on_submit():
        new_metric = BodyMetric(
            user_id=current_user.id,
            date=form.date.data,
            weight=form.weight.data,
            body_fat=form.body_fat.data
        )
        db.session.add(new_metric)
        db.session.commit()
        flash('Body metrics saved successfully.', 'success')
        return redirect(url_for('main.metrics'))

    history = BodyMetric.query.filter_by(user_id=current_user.id).order_by(BodyMetric.date.desc()).all()
    return render_template('main/metrics.html', form=form, history=history)


@main_bp.route('/workouts', methods=['GET', 'POST'])
@login_required
def workouts():
    """Handles workout logging and volume history."""
    form = WorkoutLogForm()
    if form.validate_on_submit():
        new_workout = WorkoutLog(
            user_id=current_user.id,
            exercise_name=form.exercise_name.data,
            muscle_group=form.muscle_group.data,
            intensity=form.intensity.data,
            sets=form.sets.data,
            reps=form.reps.data,
            weight=form.weight.data
        )
        db.session.add(new_workout)
        db.session.commit()
        flash('Workout logged successfully.', 'success')
        return redirect(url_for('main.workouts'))

    history = WorkoutLog.query.filter_by(user_id=current_user.id) \
        .order_by(WorkoutLog.date.desc()).all()

    return render_template('main/workouts.html', form=form, workouts=history)


@main_bp.route('/export/workouts')
@login_required
def export_workouts():
    """Generates and returns a CSV file of the user's full workout history."""
    workouts = WorkoutLog.query.filter_by(user_id=current_user.id) \
        .order_by(WorkoutLog.date.desc()).all()
    
    if not workouts:
        flash('No workout data available to export.', 'warning')
        return redirect(url_for('main.workouts'))

    csv_body = generate_workout_csv(workouts)
    
    return Response(
        csv_body,
        mimetype="text/csv",
        headers={
            "Content-disposition": "attachment; filename=workout_history.csv",
        }
    )

@main_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """Handles user profile updates (Issue #130)."""
    form = EditProfileForm()
    
    if form.validate_on_submit():
        # Update current_user object with form data
        current_user.gender = form.gender.data
        current_user.birth_date = form.birth_date.data
        current_user.height = form.height.data
        current_user.weight = form.weight.data
        
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('main.profile'))
        
    elif request.method == 'GET':
        # Pre-fill form with existing user data
        form.email.data = current_user.email
        form.gender.data = current_user.gender
        form.birth_date.data = current_user.birth_date
        form.height.data = current_user.height
        form.weight.data = current_user.weight
        
    return render_template('main/profile.html', title='Profile Settings', form=form)