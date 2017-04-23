from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField



class ContactForm(FlaskForm):
    first_name = StringField('First name')
    last_name = StringField('Last name')
    email = StringField('Email')
    organisation = StringField('Organisation')
    message = TextAreaField('Your message')
