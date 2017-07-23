from flask_wtf import FlaskForm
from wtforms import DecimalField, SelectField, TextField

class GreyscaleLevelsForm(FlaskForm):
    levels = SelectField(choices=[(x, x) for x in range(13)], coerce=int)


class ObserverInformationForm(FlaskForm):
    age = DecimalField(description="What is your age?")
    gender = SelectField(choices=[('na', 'No answer'), ('f', 'Female'), ('m', 'Male'), ('t', 'Transgender')])


class ColourVisionForm(FlaskForm):
    tests_complete = DecimalField()
    tests_correct = DecimalField()


class ColourNameForm(FlaskForm):
    name = TextField()
