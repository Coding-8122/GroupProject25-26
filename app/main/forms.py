from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class RecoveryLogForm(FlaskForm):
    """Form for daily recovery metrics tracking."""
    sleep_hours = FloatField('Sleep Hours', validators=[DataRequired(), NumberRange(0, 24)])
    muscle_soreness = IntegerField('Soreness (1-10)', validators=[DataRequired(), NumberRange(1, 10)])
    energy_level = IntegerField('Energy (1-10)', validators=[DataRequired(), NumberRange(1, 10)])
    stress_level = IntegerField('Stress (1-10)', validators=[DataRequired(), NumberRange(1, 10)])
    submit = SubmitField('Log Recovery')

class WorkoutLogForm(FlaskForm):
    """Form for logging a single exercise entry."""
    exercise_name = StringField('Exercise', validators=[DataRequired()])
    sets = IntegerField('Sets', validators=[DataRequired(), NumberRange(min=1)])
    reps = IntegerField('Reps', validators=[DataRequired(), NumberRange(min=1)])
    weight = FloatField('Weight (kg)', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Add Exercise')