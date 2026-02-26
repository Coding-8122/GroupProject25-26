from flask import render_template
from flask_login import login_required, current_user
from app.main import main_bp
from app.models.recovery import RecoveryLog


@main_bp.route('/')
@main_bp.route('/dashboard')
@login_required
def dashboard():
    """
    Main dashboard view.
    Fetches the latest recovery entries and calculates a basic recovery score.
    """
    # Fetch last 7 logs for the chart/list
    recent_logs = RecoveryLog.query.filter_by(user_id=current_user.id) \
        .order_by(RecoveryLog.date.desc()) \
        .limit(7).all()

    # Default score if no logs exist
    recovery_score = 0

    if recent_logs:
        latest = recent_logs[0]
        # Heuristic recovery score logic:
        # Sleep (50% weight), Muscle State (30% weight), Energy (20% weight)
        sleep_factor = min(latest.sleep_hours / 8, 1.2) * 50  # Cap at 8h for calculation
        soreness_factor = (10 - latest.muscle_soreness) * 3
        energy_factor = latest.energy_level * 2

        recovery_score = round(sleep_factor + soreness_factor + energy_factor)
        # Ensure score stays within 0-100 range
        recovery_score = max(0, min(100, recovery_score))

    return render_template(
        'main/dashboard.html',
        title='Dashboard',
        logs=recent_logs,
        score=recovery_score
    )


@main_bp.route('/body-metrics')
@login_required
def body_metrics():
    """View for historical body weight and height tracking."""
    return render_template('main/body_metrics.html', title='Body Metrics')