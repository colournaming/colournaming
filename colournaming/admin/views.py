"""Views for the namer."""

from flask import Blueprint, render_template, Response
from .controller import get_responses, get_particants

bp = Blueprint('admin', __name__)


@bp.route('/')
def index():
    """Menu of admin functions."""
    return render_template('admin_menu.html')

@bp.route('/responses.csv')
def show_responses():
    """Return experiment responses as CSV."""
    return Response(get_responses(), mimetype='text/csv')

@bp.route('/participants.csv')
def show_responses():
    """Return participants as CSV."""
    return Response(get_participants(), mimetype='text/csv')
