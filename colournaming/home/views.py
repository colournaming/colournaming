"""Views for the front page."""

from flask import Blueprint, current_app, render_template
from flask_mail import Message
from ..email import mail
from .forms import ContactForm

bp = Blueprint('home', __name__)


@bp.route('/')
def index():
    """Render the front page."""
    return render_template('index.html')


@bp.route('research.html')
def research():
    """Render the research page."""
    return render_template('research.html')


@bp.route('terms_and_conditions.html')
def terms_and_conditions():
    """Render the terms and conditions page."""
    return render_template('terms_and_conditions.html')


@bp.route('contact.html')
def contact():
    """Render the contact page."""
    form = ContactForm()
    if form.validate_on_submit():
        msg = Message(
            'ColourNamer message from {0} {1}'.format(form.first_name, form.last_name),
            sender='contact@colornaming.net',
            recipients=[current_app.config['CONTACT_EMAIL']]
        )
        msg.body = (
            'FROM: {0} {1} <{2}>\n'
            'ORGANISATION: {3}\n\n'
            '{4}'
        )
        mail.send(msg)
    return render_template('contact.html', form=form)
