"""Forms used by the colour namer."""

from flask_wtf import FlaskForm
from wtforms import DecimalField, SelectField, StringField, validators
from ..experiment.forms import _enum_to_choices
from . import model


class NameAgreementForm(FlaskForm):
    """Form for colour name agreement."""

    language_code = StringField(validators=[validators.length(min=2, max=2)])
    red = DecimalField()
    green = DecimalField()
    blue = DecimalField()
    agreement = SelectField(
        choices=_enum_to_choices(model.AgreementLevel),
    )
