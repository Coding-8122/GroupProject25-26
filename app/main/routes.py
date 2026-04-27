import bleach
from flask import render_template, url_for, flash, redirect, request, jsonify, Response
from flask_login import login_required, current_user
from sqlalchemy import func
from collections import defaultdict
from app import limiter
from app.main import main_bp
from app.extensions import db
from app.models.workout import WorkoutLog
from app.models.body_metric import BodyMetric
from app.models.recovery import RecoveryLog
from app.main.forms import (
    RecoveryLogForm,
    WorkoutLogForm,
    BodyMetricsForm,
    EditProfileForm,
)
from datetime import datetime, timezone
from app.utils.recovery_calculations import calculate_recovery_hours
from app.utils.export_utils import generate_workout_csv


def _sanitize(text: str) -> str:
    """Strip HTML tags to prevent XSS."""
    return bleach.clean(text, tags=[], strip=True).strip()


@main_bp.route("/", methods=["GET", "POST"])
@main_bp.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    form = RecoveryLogForm()
    today = datetime.now(timezone.utc).date()
    last_workout = (
        WorkoutLog.query.filter_by(user_id=current_user.id)
        .order_by(WorkoutLog.date.desc())
        .first()
    )

    if form.validate_on_submit():
        log = RecoveryLog.query.filter_by(user_id=current_user.id, date=today).first()
        if not log:
            log = RecoveryLog(user_id=current_user.id, date=today)
            db.session.add(log)

        log.sleep_hours = form.sleep_hours.data
        log.muscle_soreness = form.muscle_soreness.data
        max_int = (
            db.session.query(func.max(WorkoutLog.intensity))
            .filter(WorkoutLog.user_id == current_user.id, WorkoutLog.date == today)
            .scalar()
        )

        log.recovery_estimated = calculate_recovery_hours(
            max_int or 5, log.muscle_soreness, log.sleep_hours
        )
        db.session.commit()
        flash("Metrics updated.", "success")
        return redirect(url_for("main.dashboard"))

    recent_logs = (
        RecoveryLog.query.filter_by(user_id=current_user.id)
        .order_by(RecoveryLog.date.desc())
        .limit(7)
        .all()
    )
    return render_template(
        "main/dashboard.html", form=form, logs=recent_logs, last_workout=last_workout
    )


@main_bp.route("/metrics", methods=["GET", "POST"])
@login_required
def metrics():
    """Handles weight tracking and syncs user profile."""
    form = BodyMetricsForm()
    if form.validate_on_submit():
        new_metric = BodyMetric(
            user_id=current_user.id,
            date=form.date.data,
            weight=form.weight.data,
            body_fat=form.body_fat.data,
        )
        db.session.add(new_metric)
        current_user.weight = form.weight.data
        db.session.commit()
        flash("Body metrics saved!", "success")
        return redirect(url_for("main.metrics"))

    history = (
        BodyMetric.query.filter_by(user_id=current_user.id)
        .order_by(BodyMetric.date.desc())
        .all()
    )
    chart_data = (
        BodyMetric.query.filter_by(user_id=current_user.id)
        .order_by(BodyMetric.date.asc())
        .all()
    )
    weight_change = (
        round(chart_data[-1].weight - chart_data[0].weight, 2)
        if len(chart_data) >= 2
        else 0
    )
    return render_template(
        "main/metrics.html", form=form, history=history, weight_change=weight_change
    )


@main_bp.route("/api/stats/weight")
@login_required
@limiter.limit("60 per minute")
def api_weight():
    metrics = (
        BodyMetric.query.filter_by(user_id=current_user.id)
        .order_by(BodyMetric.date.asc())
        .all()
    )
    return jsonify(
        {
            "labels": [m.date.strftime("%b %d") for m in metrics],
            "weight": [m.weight for m in metrics],
            "fat": [m.body_fat for m in metrics if m.body_fat is not None],
        }
    )


@main_bp.route("/api/stats/volume")
@login_required
def api_volume():
    workouts = WorkoutLog.query.filter_by(user_id=current_user.id).all()
    vol = defaultdict(float)
    for w in workouts:
        vol[w.muscle_group] += w.sets * w.reps * w.weight
    return jsonify({"labels": list(vol.keys()), "data": list(vol.values())})


@main_bp.route("/workouts", methods=["GET", "POST"])
@login_required
def workouts():
    form = WorkoutLogForm()
    if form.validate_on_submit():
        nw = WorkoutLog(
            user_id=current_user.id,
            exercise_name=_sanitize(form.exercise_name.data),
            muscle_group=form.muscle_group.data,
            intensity=form.intensity.data,
            sets=form.sets.data,
            reps=form.reps.data,
            weight=form.weight.data,
        )
        db.session.add(nw)
        db.session.commit()
        flash("Workout logged successfully.", "success")
        return redirect(url_for("main.workouts"))
    history = (
        WorkoutLog.query.filter_by(user_id=current_user.id)
        .order_by(WorkoutLog.date.desc())
        .all()
    )
    return render_template("main/workouts.html", form=form, workouts=history)


@main_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """FIX: Added missing profile endpoint for 'main.profile'."""
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.height = form.height.data
        current_user.weight = form.weight.data
        db.session.commit()
        flash("Profile updated!", "success")
        return redirect(url_for("main.profile"))
    elif request.method == "GET":
        form.email.data = current_user.email
        form.height.data = current_user.height
        form.weight.data = current_user.weight
    return render_template("main/profile.html", title="Profile Settings", form=form)


@main_bp.route("/export/workouts")
@login_required
def export_workouts():
    workouts = (
        WorkoutLog.query.filter_by(user_id=current_user.id)
        .order_by(WorkoutLog.date.desc())
        .all()
    )
    if not workouts:
        flash("No data available.", "warning")
        return redirect(url_for("main.workouts"))
    csv_body = generate_workout_csv(workouts)
    return Response(
        csv_body,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=history.csv"},
    )
