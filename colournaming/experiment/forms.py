"""Forms used in the colour naming experiment."""

from flask_wtf import FlaskForm
import pycountry
from wtforms import BooleanField, DecimalField, HiddenField, IntegerField, SelectField, TextField
from wtforms.validators import DataRequired, Optional
from wtforms.widgets import HiddenInput
from . import model

def _enum_to_choices(enum):
    choices = [(x.name, x.name.replace('_', ' ').capitalize()) for x in enum]
    return [('', '-')] + choices


class DisplayForm(FlaskForm):
    """Form for gathering display information."""
    levels = SelectField(
        choices=[(x, x) for x in range(13)],
        coerce=int,
        description="How many steps can you see in the greyscale ramp?",
        validators=[Optional()]
    )
    screen_height = IntegerField(widget=HiddenInput())
    screen_width = IntegerField(widget=HiddenInput())
    screen_colour_depth = IntegerField(widget=HiddenInput())


class ObserverInformationForm(FlaskForm):
    """Form for gathering observer information."""

    age_choices = [(-1, '-')] + list(zip(range(16, 100), range(16, 100)))
    age = SelectField(
        choices=age_choices,
        description="What is your age?",
        coerce=int,
        validators=[Optional()]
    )
    gender = SelectField(
        choices=_enum_to_choices(model.Gender),
        description="What is your gender?",
        validators=[Optional()]
    )
    colour_experience = SelectField(
        choices=_enum_to_choices(model.ColourExperience),
        description="What level of experience do you have working with colour?",
        validators=[Optional()]
    )
    language_experience = SelectField(
        choices=_enum_to_choices(model.LanguageExperience),
        description="What experience do you have with your language?",
        validators=[Optional()]
    )
    education_level = SelectField(
        choices=_enum_to_choices(model.EducationLevel),
        description="What level of education have you attained?",
        validators=[Optional()]
    )
    country_choices = [('', '-')] + \
        sorted([(x.alpha_2, x.name) for x in pycountry.countries], key=lambda x: x[1])
    country_raised = SelectField(
        choices=country_choices,
        description="In which country were you raised?",
        validators=[Optional()]
    )
    country_resident = SelectField(
        choices=country_choices,
        description="In which country are you currently living?",
        validators=[Optional()]
    )
    ambient_light = SelectField(
        choices=_enum_to_choices(model.AmbientLight),
        description="What is the level of ambient lighting where you are?",
        validators=[Optional()]
    )
    screen_light = SelectField(
        choices=_enum_to_choices(model.ScreenLight),
        description="What is the lighting level behind your screen?",
        validators=[Optional()]
    )
    distance_choices = [(-1, '-')] + list(zip(range(30, 70, 10), range(30, 70, 10))) + [(999, '80+')]
    screen_distance = SelectField(
        choices=distance_choices,
        description="What distance are you from your monitor in cm?",
        coerce=float,
        validators=[Optional()]
    )


class ColourVisionForm(FlaskForm):
    """Form for gathering colour vision performance."""

    square_disappeared = BooleanField(
        validators=[Optional()]
    )


class ColourNameForm(FlaskForm):
    """Form for recording a colour name response."""

    name = TextField(
        validators=[DataRequired()]
    )
    target_id = IntegerField(
        validators=[DataRequired()]
    )
    response_time = DecimalField()
