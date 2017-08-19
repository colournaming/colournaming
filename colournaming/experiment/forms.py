"""Forms used in the colour naming experiment."""

from flask_wtf import FlaskForm
from wtforms import DecimalField, HiddenField, SelectField, TextField
from wtforms.widgets import HiddenInput
from . import model

def _enum_to_choices(enum):
    return [(x.value, x.name) for x in enum]


class DisplayForm(FlaskForm):
    """Form for gathering display information."""

    levels = SelectField(choices=[(x, x) for x in range(13)], coerce=int)
    screen_height = HiddenField()
    screen_width = HiddenField()
    device_orientation = DecimalField(widget=HiddenInput())
    ambient_light = SelectField(choices=_enum_to_choices(model.AmbientLight))
    screen_light = SelectField(choices=_enum_to_choices(model.ScreenLight))


class ObserverInformationForm(FlaskForm):
    """Form for gathering observer information."""

    age = DecimalField(description="What is your age?")
    gender = SelectField(choices=_enum_to_choices(model.Gender))
    colour_experience = SelectField(choices=_enum_to_choices(model.ColourExperience))
    language_experience = SelectField(choices=_enum_to_choices(model.LanguageExperience))
    education_level = SelectField(choices=_enum_to_choices(model.EducationLevel))


class ColourVisionForm(FlaskForm):
    """Form for gathering colour vision performance."""

    tests_complete = DecimalField()
    tests_correct = DecimalField()
    colour_vision_status = SelectField(choices=_enum_to_choices(model.ColourVision), coerce=int)


class ColourNameForm(FlaskForm):
    """Form for recording a colour name response."""

    name = TextField()
    response_time_ms = DecimalField()
