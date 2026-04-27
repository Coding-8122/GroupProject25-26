from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired, NumberRange, Optional
from datetime import datetime, timezone

class RecoveryLogForm(FlaskForm):
    sleep_hours = FloatField('Sleep Hours', validators=[
        DataRequired(),
        NumberRange(0, 24, message="Sleep must be between 0 and 24 hours")
    ])
    muscle_soreness = IntegerField('Soreness (1-10)', validators=[
        DataRequired(),
        NumberRange(1, 10, message="Soreness must be between 1 and 10")
    ])
    energy_level = IntegerField('Energy (1-10)', validators=[
        DataRequired(),
        NumberRange(1, 10, message="Energy must be between 1 and 10")
    ])
    stress_level = IntegerField('Stress (1-10)', validators=[
        DataRequired(),
        NumberRange(1, 10, message="Stress must be between 1 and 10")
    ])
    submit = SubmitField('Log Recovery')

class WorkoutLogForm(FlaskForm):
    exercise_name = StringField('Exercise', validators=[DataRequired()])
    muscle_group = SelectField('Muscle Group', choices=[
        ('Chest', 'Chest'), ('Back', 'Back'), ('Legs', 'Legs'),
        ('Shoulders', 'Shoulders'), ('Arms', 'Arms'), ('Core', 'Core'), ('Full Body', 'Full Body')
    ], validators=[DataRequired()])
    intensity = IntegerField('Intensity (RPE 1-10)', validators=[
        DataRequired(),
        NumberRange(1, 10, message="RPE must be between 1 and 10")
    ])
    sets = IntegerField('Sets', validators=[
        DataRequired(),
        NumberRange(min=1, message="Sets must be at least 1")
    ])
    reps = IntegerField('Reps', validators=[
        DataRequired(),
        NumberRange(min=1, message="Reps must be at least 1")
    ])
    weight = FloatField('Weight (kg)', validators=[
        DataRequired(),
        NumberRange(min=0, message="Weight must be positive")
    ])
    submit = SubmitField('Add Exercise')

class BodyMetricsForm(FlaskForm):
    date = DateField('Date', default=lambda: datetime.now(timezone.utc).date(), validators=[DataRequired()])
    weight = FloatField('Weight (kg)', validators=[
        DataRequired(),
        NumberRange(min=10, max=500, message="Weight must be between 10 and 500 kg")
    ])
    body_fat = FloatField('Body Fat %', validators=[
        Optional(),
        NumberRange(0, 100, message="Body fat must be between 0 and 100")
    ])
    submit = SubmitField('Save Check-in')