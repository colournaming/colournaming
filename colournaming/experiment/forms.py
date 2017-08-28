"""Forms used in the colour naming experiment."""

from flask_wtf import FlaskForm
import pycountry
from wtforms import DecimalField, HiddenField, SelectField, TextField
from wtforms.validators import DataRequired
from wtforms.widgets import HiddenInput
from . import model

def _enum_to_choices(enum):
    return [(x.value, x.name) for x in enum]


class DisplayForm(FlaskForm):
    """Form for gathering display information."""

    levels = SelectField(
        choices=[(x, x) for x in range(13)], 
        coerce=int,
        description="How many steps can you see in the greyscale ramp?"
    )
    screen_height = HiddenField()
    screen_width = HiddenField()
    screen_colour_depth = HiddenField()
    ambient_light = SelectField(
        choices=_enum_to_choices(model.AmbientLight),
        coerce=int,
        description="What is the level of ambient lighting where you are?"
    )
    screen_light = SelectField(
        choices=_enum_to_choices(model.ScreenLight),
        coerce=int,
        description="What is the lighting level behind your screen?"
    )


class ObserverInformationForm(FlaskForm):
    """Form for gathering observer information."""

    age = DecimalField(description="What is your age?")
    gender = SelectField(
        choices=_enum_to_choices(model.Gender),
        coerce=int,
        description="What is your gender?"
    )
    colour_experience = SelectField(
        choices=_enum_to_choices(model.ColourExperience),
        coerce=int,
        description="What level of experience do you have working with colour?"
    )
    language_experience = SelectField(
        choices=_enum_to_choices(model.LanguageExperience),
        coerce=int,
        description="What experience do you have with your language?"
    )
    education_level = SelectField(
        choices=_enum_to_choices(model.EducationLevel),
        coerce=int,
        description="What level of education have you attained?"
    )
    user_agent = HiddenField()
    ip_address = HiddenField()
    country_raised = SelectField(
        choices=[(x.alpha_2, x.name) for x in pycountry.countries],
        description="In which country were you raised?"
    )
    country_resident = SelectField(
        choices=[(x.alpha_2, x.name) for x in pycountry.countries],
        description="In which country are you currently living?"
    )


class ColourVisionForm(FlaskForm):
    """Form for gathering colour vision performance."""

    tests_complete = DecimalField()
    tests_correct = DecimalField()
    colour_vision_status = SelectField(
        choices=_enum_to_choices(model.ColourVision),
        coerce=int
    )


class ColourNameForm(FlaskForm):
    """Form for recording a colour name response."""

    name = TextField(
        validators=[DataRequired()]
    )
    target_id = DecimalField(
        validators=[DataRequired()]
    )
    response_time_ms = DecimalField()
