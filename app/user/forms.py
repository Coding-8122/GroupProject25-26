from flask_wtf import FlaskForm
from wtforms import FloatField, SelectField, DateField, SubmitField
from wtforms.validators import Optional, NumberRange


class UpdateProfileForm(FlaskForm):
    """Form for updating user profile metrics with strict validation."""
    gender = SelectField('Gender', choices=[
        ('', 'Select...'), ('male', 'Male'), ('female', 'Female'), ('other', 'Other')
    ], validators=[Optional()])

    birth_date = DateField('Birth Date', format='%Y-%m-%d', validators=[Optional()])

    # Ensure height is a positive, realistic value
    height = FloatField('Height (cm)', validators=[
        Optional(),
        NumberRange(min=50.0, max=250.0, message="Height must be between 50 and 250 cm")
    ])

    # Prevent negative weight or unrealistic values
    weight = FloatField('Weight (kg)', validators=[
        Optional(),
        NumberRange(min=10.0, max=500.0, message="Weight must be between 10 and 500 kg")
    ])

    submit = SubmitField('Update Profile')