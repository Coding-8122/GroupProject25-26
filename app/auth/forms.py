from flask import current_app
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, DateField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Optional, Length
import sqlalchemy as sa
from app.models.user import User
from app.extensions import db


class RegistrationForm(FlaskForm):
    """Form for user registration with robust validation."""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message="Password must be at least 8 characters."),
    ])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])

    # Added Optional() to prevent validation crashes on empty submissions
    height = FloatField('Height (cm)', validators=[Optional()])
    weight = FloatField('Weight (kg)', validators=[Optional()])
    birth_date = DateField('Birth Date (YYYY-MM-DD)', format='%Y-%m-%d', validators=[Optional()])

    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        """
        Custom validator to ensure the email is unique in the database.
        Uses modern SQLAlchemy 2.0 query syntax.
        """
        user = db.session.scalar(sa.select(User).filter_by(email=email.data.lower().strip()))
        if user:
            raise ValidationError('That email is already taken. Please choose a different one.')

    def validate_password(self, password):
        """
        Enforce password complexity requirements:
        at least one uppercase, one lowercase, one digit, one special character.
        """
        policy = current_app.config.get('PASSWORD_COMPLEXITY_RE')
        if policy and not policy.match(password.data):
            raise ValidationError(
                'Password must include uppercase, lowercase, a digit, and a special character.'
            )


class LoginForm(FlaskForm):
    """Standard user login form."""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')