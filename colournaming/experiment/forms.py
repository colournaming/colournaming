from flask_wtf import FlaskForm
from wtforms import DecimalField, SelectField

class GreyscaleLevelsForm(FlaskForm):
    levels = SelectField(choices=[(x, x) for x in range(13)], coerce=int)


class ObserverInformation(FlaskForm):
    age = DecimalField(description="What is your age?")
    gender = SelectField(choices=[('na', 'No answer'), ('f', 'Female'), ('m', 'Male'), ('t', 'Transgender')])
