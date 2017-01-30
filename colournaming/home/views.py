"""Views for the front page."""

from flask import Blueprint, render_template

bp = Blueprint('home', __name__, url_prefix='/')


@bp.route('/')
def index():
    """Render the front page."""
    return render_template('index.html')


@bp.route('terms_and_conditions.html')
def terms_and_conditions():
    """Render the terms and conditions page."""
    return render_template('terms_and_conditions.html')
