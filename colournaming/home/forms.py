from flask_babel import lazy_gettext
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField


class ContactForm(FlaskForm):
    first_name = StringField(lazy_gettext('First name'))
    last_name = StringField(lazy_gettext('Last name'))
    email = StringField(lazy_gettext('Email'))
    organisation = StringField(lazy_gettext('Organisation'))
    message = TextAreaField(lazy_gettext('Your message'))
