from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField


class LoginForm(FlaskForm):
    """Form for gathering display information."""

    username = StringField()
    password = PasswordField()
