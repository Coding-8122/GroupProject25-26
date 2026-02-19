from flask_wtf import FlaskForm
from wtforms import FloatField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional


class UpdateProfileForm(FlaskForm):
    # Gender selection as a dropdown
    gender = SelectField('Gender', choices=[
        ('', 'Select...'),
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], validators=[Optional()])

    birth_date = DateField('Birth Date', format='%Y-%m-%d', validators=[Optional()])
    height = FloatField('Height (cm)', validators=[Optional()])
    weight = FloatField('Weight (kg)', validators=[Optional()])
    submit = SubmitField('Update Profile')
