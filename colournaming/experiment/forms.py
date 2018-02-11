"""Forms used in the colour naming experiment."""

from flask_wtf import FlaskForm
from flask_babel import lazy_gettext
import pycountry
from wtforms import BooleanField, DecimalField, HiddenField, IntegerField, SelectField, TextField
from wtforms.validators import DataRequired, Optional
from wtforms.widgets import HiddenInput
from . import model


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

    location = TextField(widget=HiddenInput())
    age_choices = [(-1, '-')] + list(zip(range(16, 100), range(16, 100)))
    age = SelectField(
        choices=age_choices,
        description=lazy_gettext("What is your age?"),
        coerce=int,
        validators=[Optional()]
    )
    gender = SelectField(
        choices=[
            ('', '-'),
            ('female', lazy_gettext('Female')),
            ('male', lazy_gettext('Male')),
            ('other', lazy_gettext('Other'))
        ],
        description=lazy_gettext("To which gender do you most identify?"),
        validators=[Optional()]
    )
    gender_other = TextField(
        description=lazy_gettext("Please specify"),
        validators=[Optional()]
    )
    colour_experience = SelectField(
        choices = [
            ('', '-'),
            ('beginner', lazy_gettext('Beginner')),
            ('intermediate', lazy_gettext('Intermediate')),
            ('advanced', lazy_gettext('Advanced'))
        ],
        description=lazy_gettext("Describe your experience working with colour"),
        validators=[Optional()]
    )
    language_experience = SelectField(
        choices = [
            ('', '-'),
            ('beginner', lazy_gettext('Beginner')),
            ('intermediate', lazy_gettext('Intermediate')),
            ('advanced', lazy_gettext('Advanced')),
            ('bilingual', lazy_gettext('Bilingual')),
            ('native_speaker', lazy_gettext('Native speaker'))
        ],
        description=lazy_gettext("Describe your skill in the language used in this experiment"),
        validators=[Optional()]
    )
    education_level = SelectField(
        choices = [
            ('', '-'),
            ('no_qualifications', lazy_gettext('No qualifications')),
            ('secondary_school_degree', lazy_gettext('Secondary school degree')),
            ('bachelors_degree', lazy_gettext('Bachelors degree')),
            ('masters_degree', lazy_gettext('Masters degree')),
            ('professional_degree', lazy_gettext('Professional degree')),
            ('doctorate_degree', lazy_gettext('Doctorate degree'))
        ],
        description=lazy_gettext("What is the highest level of education you have completed?"),
        validators=[Optional()]
    )
    country_choices = [('', '-')] + \
        sorted([(x.alpha_2, x.name) for x in pycountry.countries], key=lambda x: x[1])
    country_raised = SelectField(
        choices=country_choices,
        description=lazy_gettext("In which country did you grow up?"),
        validators=[Optional()]
    )
    country_resident = SelectField(
        choices=country_choices,
        description=lazy_gettext("Where are you living?"),
        validators=[Optional()]
    )
    display_device = SelectField(
        choices = [
            ('', '-'),
            ('smartphone', lazy_gettext('Smartphone')),
            ('pad', lazy_gettext('Pad')),
            ('laptop', lazy_gettext('Laptop')),
            ('desktop', lazy_gettext('Desktop'))
        ],
        description=lazy_gettext("What is your display device?"),
        validators=[Optional()]
    )
    screen_temperature = SelectField(
        choices = [
            ('', '-'),
            ('neutral_white', lazy_gettext('Neutral white')),
            ('warm_white', lazy_gettext('Warm white')),
            ('bluish_white', lazy_gettext('Bluish white')),
            ('yellowish_white', lazy_gettext('Yellowish white'))
        ],
        description=lazy_gettext("Describe the white graphic elements on your screen"),
        validators=[Optional()]
    )
    screen_light = SelectField(
        choices = [
            ('', '-'),
            ('dark', lazy_gettext('Dark')),
            ('dim', lazy_gettext('Dim')),
            ('average', lazy_gettext('Average')),
            ('bright', lazy_gettext('Bright'))
        ],
        description=lazy_gettext("Describe the surrounding environment behind your device"),
        validators=[Optional()]
    )
    ambient_light = SelectField(
        choices = [
            ('', '-'),
            ('dark', lazy_gettext('Dark')),
            ('typical_domestic', lazy_gettext('Typical domestic')),
            ('mid_daylight', lazy_gettext('Mid daylight')),
            ('full_daylight', lazy_gettext('Full daylight')),
            ('typical_office', lazy_gettext('Typical office'))
        ],
        description=lazy_gettext("Describe the lighting conditions of your environment"),
        validators=[Optional()]
    )
    distance_choices = [(-1, '-')] + list(zip(range(10, 100, 10), range(10, 100, 10))) + [(999, '100+')]
    screen_distance = SelectField(
        choices=distance_choices,
        description=lazy_gettext("What distance are you from your monitor in cm?"),
        coerce=float,
        validators=[Optional()]
    )


class ColourVisionForm(FlaskForm):
    """Form for gathering colour vision performance."""

    square_disappeared = SelectField(
        choices=[
            ('-', '-'),
            ('no', lazy_gettext('No')),
            ('yes', lazy_gettext('Yes'))
        ],
        description=lazy_gettext("What distance are you from your monitor in cm?"),
        coerce=float,
        validators=[Optional()]
    )
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
