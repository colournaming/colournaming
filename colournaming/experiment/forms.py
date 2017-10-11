"""Forms used in the colour naming experiment."""

from flask_wtf import FlaskForm
import pycountry
from wtforms import BooleanField, DecimalField, HiddenField, IntegerField, SelectField, TextField
from wtforms.validators import DataRequired
from wtforms.widgets import HiddenInput
from . import model

def _enum_to_choices(enum):
    return [('', '-')] + [(x.name, x.name.replace('_', ' ').capitalize()) for x in enum]


class DisplayForm(FlaskForm):
    """Form for gathering display information."""
    levels = SelectField(
        choices=[(x, x) for x in range(13)],
        coerce=int,
        description="How many steps can you see in the greyscale ramp?"
    )
    screen_height = IntegerField(widget=HiddenInput())
    screen_width = IntegerField(widget=HiddenInput())
    screen_colour_depth = IntegerField(widget=HiddenInput())


class ObserverInformationForm(FlaskForm):
    """Form for gathering observer information."""

    age_choices = [('-1', '-')] + list(zip(range(16, 100), range(16, 100)))
    age = SelectField(
        choices=age_choices,
        description="What is your age?",
        coerce=int
    )
    gender = SelectField(
        choices=_enum_to_choices(model.Gender),
        description="What is your gender?"
    )
    colour_experience = SelectField(
        choices=_enum_to_choices(model.ColourExperience),
        description="What level of experience do you have working with colour?"
    )
    language_experience = SelectField(
        choices=_enum_to_choices(model.LanguageExperience),
        description="What experience do you have with your language?"
    )
    education_level = SelectField(
        choices=_enum_to_choices(model.EducationLevel),
        description="What level of education have you attained?"
    )
    country_raised = SelectField(
        choices=[('', '-')] + [(x.alpha_2, x.name) for x in pycountry.countries],
        description="In which country were you raised?"
    )
    country_resident = SelectField(
        choices=[('', '-')] + [(x.alpha_2, x.name) for x in pycountry.countries],
        description="In which country are you currently living?"
    )
    ambient_light = SelectField(
        choices=_enum_to_choices(model.AmbientLight),
        description="What is the level of ambient lighting where you are?"
    )
    screen_light = SelectField(
        choices=_enum_to_choices(model.ScreenLight),
        description="What is the lighting level behind your screen?"
    )
    distance_choices = [('-1', '-')] + list(zip(range(30, 70, 10), range(30, 70, 10))) + [('999', '80+')]
    screen_distance = SelectField(
        choices=distance_choices,
        description="What distance are you from your monitor in cm?",
        coerce=float
    )


class ColourVisionForm(FlaskForm):
    """Form for gathering colour vision performance."""

    square_disappeared =  BooleanField()


class ColourNameForm(FlaskForm):
    """Form for recording a colour name response."""

    name = TextField(
        validators=[DataRequired()]
    )
    target_id = IntegerField(
        validators=[DataRequired()]
    )
    response_time = DecimalField()
