"""Views for the front page."""

from flask import Blueprint, render_template
from .forms import ContactForm

bp = Blueprint('home', __name__)


@bp.route('/')
def index():
    """Render the front page."""
    return render_template('index.html')


@bp.route('terms_and_conditions.html')
def terms_and_conditions():
    """Render the terms and conditions page."""
    return render_template('terms_and_conditions.html')

@bp.route('contact.html')
def contact():
    """Render the contact page."""
    form = ContactForm()
    if form.validate_on_submit():
        pass
    return render_template('contact.html', form=form)
