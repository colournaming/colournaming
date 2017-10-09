"""Views for the namer."""

from flask import Blueprint, render_template
from .controller import get_responses

bp = Blueprint('admin', __name__)


@bp.route('/')
def index():
    """Menu of admin functions."""
    return render_template('admin_menu.html')

@bp.route('/responses.csv')
def show_responses():
    """Return experiment responses as CSV."""
    return get_responses()
