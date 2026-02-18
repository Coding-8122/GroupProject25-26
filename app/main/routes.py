from flask import render_template
from flask_login import login_required
from flask import Blueprint

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('main/dashboard.html', title='Dashboard')

@main_bp.route('/body-metrics')
@login_required
def body_metrics():
    return render_template('main/body_metrics.html', title='Body Metrics')