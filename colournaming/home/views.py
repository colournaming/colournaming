"""Views for the front page."""

from flask import Blueprint, current_app, render_template
from flask_mail import Message
from ..email import mail
from .forms import ContactForm
from ..namer import controller as namer_controller
from ..namer.forms import NameAgreementForm

bp = Blueprint('home', __name__)


@bp.route('/', methods=['GET', 'POST'])
def index():
    """Render the front page."""
    contact_form = ContactForm()
    name_agreement_form = NameAgreementForm()
    if contact_form.validate_on_submit():
        msg = Message(
            'ColourNamer message from {0} {1}'.format(contact_form.first_name, contact_form.last_name),
            sender='contact@colornaming.net',
            recipients=[current_app.config['CONTACT_EMAIL']]
        )
        msg_text = 'FROM: {0} {1} <{2}>\nORGANISATION: {3}\n\n{4}'.format(
            contact_form.first_name.data,
            contact_form.last_name.data,
            contact_form.email.data,
            contact_form.organisation.data,
            contact_form.message.data,
        )
        msg.body = msg_text
        mail.send(msg)
    return render_template(
        'index.html',
        contact_form=contact_form,
        name_agreement_form=name_agreement_form,
        languages=namer_controller.language_list()
    )


@bp.route('research.html')
def research():
    """Render the research page."""
    return render_template('research.html')


@bp.route('terms_and_conditions.html')
def terms_and_conditions():
    """Render the terms and conditions page."""
    return render_template('terms_and_conditions.html')
