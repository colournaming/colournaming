from flask_wtf import FlaskForm
from wtforms import SelectField

class GreyscaleLevelsForm(FlaskForm):
    levels = SelectField(choices=[(x, x) for x in range(13)], coerce=int)
