from flask_wtf import FlaskForm
from wtforms import FloatField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class RecoveryLogForm(FlaskForm):
    """Form for users to log their daily recovery metrics."""
    sleep_hours = FloatField('Sleep Hours', validators=[
        DataRequired(),
        NumberRange(min=0, max=24, message="Sleep must be between 0 and 24 hours")
    ])
    muscle_soreness = IntegerField('Muscle Soreness (1-10)', validators=[
        DataRequired(),
        NumberRange(min=1, max=10, message="Scale is 1 (fresh) to 10 (very sore)")
    ])
    energy_level = IntegerField('Energy Level (1-10)', validators=[
        DataRequired(),
        NumberRange(min=1, max=10, message="Scale is 1 (exhausted) to 10 (full energy)")
    ])
    stress_level = IntegerField('Stress Level (1-10)', validators=[
        DataRequired(),
        NumberRange(min=1, max=10, message="Scale is 1 (calm) to 10 (very stressed)")
    ])
    submit = SubmitField('Save Log')