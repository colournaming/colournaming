"""Forms used by the colour namer."""

from flask_babel import lazy_gettext
from flask_wtf import FlaskForm
from wtforms import DecimalField, SelectField, StringField, validators
from . import model


class NameAgreementForm(FlaskForm):
    """Form for colour name agreement."""

    language_code = StringField(validators=[validators.length(min=2, max=2)])
    red = DecimalField()
    green = DecimalField()
    blue = DecimalField()
    agreement = SelectField(
        choices=[
            ("", lazy_gettext("Do you agree?")),
            ("strongly_disagree", lazy_gettext("Strongly disagree")),
            ("disagree", lazy_gettext("Disagree")),
            ("undecided", lazy_gettext("Undecided")),
            ("agree", lazy_gettext("Agree")),
            ("strongly_agree", lazy_gettext("Strongly agree")),
        ],
        default="",
    )
