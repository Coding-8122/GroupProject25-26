from flask import render_template, url_for, flash, redirect, request
from flask_login import login_required, current_user
from app.main import main_bp
from app.extensions import db
from app.models.recovery import RecoveryLog
from app.models.workout import WorkoutLog
from app.models.body_metric import BodyMetric
from app.main.forms import RecoveryLogForm, WorkoutLogForm, BodyMetricsForm
from datetime import datetime
from app.utils.recovery_calculations import calculate_recovery_hours

@main_bp.route('/', methods=['GET', 'POST'])
@main_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    """Handles recovery display and logging based on muscle-specific data."""
    form = RecoveryLogForm()

    # Get the latest workout entry for this user
    last_workout = WorkoutLog.query.filter_by(user_id=current_user.id) \
        .order_by(WorkoutLog.date.desc(), WorkoutLog.id.desc()).first()

    if form.validate_on_submit():
        today = datetime.utcnow().date()
        log = RecoveryLog.query.filter_by(user_id=current_user.id, date=today).first()
        if not log:
            log = RecoveryLog(user_id=current_user.id)
            db.session.add(log)

        log.sleep_hours = form.sleep_hours.data
        log.muscle_soreness = form.muscle_soreness.data
        log.energy_level = form.energy_level.data
        log.stress_level = form.stress_level.data

        # Use actual intensity from the latest workout, fallback to 5
        current_intensity = last_workout.intensity if last_workout else 5

        log.recovery_estimated = calculate_recovery_hours(
            intensity=current_intensity,
            soreness=log.muscle_soreness,
            sleep_hours=log.sleep_hours
        )

        db.session.commit()
        flash(f'Metrics updated! Used {last_workout.muscle_group if last_workout else "General"} intensity.', 'success')
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
        flash('Body metrics saved!', 'success')
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
        flash('Workout logged!', 'success')
        return redirect(url_for('main.workouts'))

    # Get all workouts for history display
    history = WorkoutLog.query.filter_by(user_id=current_user.id) \
        .order_by(WorkoutLog.date.desc()).all()

    return render_template('main/workouts.html', form=form, workouts=history)