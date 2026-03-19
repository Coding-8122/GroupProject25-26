from flask import render_template, url_for, flash, redirect, request
from flask_login import login_required, current_user
from app.main import main_bp
from app.extensions import db
from app.models.recovery import RecoveryLog
from app.models.workout import WorkoutLog
from app.main.forms import RecoveryLogForm, WorkoutLogForm
from datetime import datetime
from app.utils.recovery_calculations import calculate_recovery_hours


@main_bp.route('/', methods=['GET', 'POST'])
@main_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    """Handles recovery display and logging."""
    form = RecoveryLogForm()

    if form.validate_on_submit():
        today = datetime.utcnow().date()
        log = RecoveryLog.query.filter_by(user_id=current_user.id, date=today).first()
        if not log:
            log = RecoveryLog(user_id=current_user.id)
            db.session.add(log)

        # Capture the data from the form
        log.sleep_hours = form.sleep_hours.data
        log.muscle_soreness = form.muscle_soreness.data
        log.energy_level = form.energy_level.data
        log.stress_level = form.stress_level.data

        # Run the calculation logic
        # We use a default intensity of 5 until you add that field to your forms
        log.recovery_estimated = calculate_recovery_hours(
            intensity=5,
            soreness=log.muscle_soreness,
            sleep_hours=log.sleep_hours
        )

        db.session.commit()
        flash(f'Metrics updated! Estimated recovery: {log.recovery_estimated} hours.', 'success')
        return redirect(url_for('main.dashboard'))

    recent_logs = RecoveryLog.query.filter_by(user_id=current_user.id) \
        .order_by(RecoveryLog.date.desc()).limit(7).all()

    return render_template('main/dashboard.html', form=form, logs=recent_logs)


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
        flash('Workout logged!', 'success')
        return redirect(url_for('main.workouts'))

    # Get all workouts for history
    history = WorkoutLog.query.filter_by(user_id=current_user.id) \
        .order_by(WorkoutLog.date.desc()).all()

    return render_template('main/workouts.html', form=form, workouts=history)