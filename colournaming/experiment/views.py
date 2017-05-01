"""Views for the experiment."""

from flask import Blueprint

bp = Blueprint('experiment', __name__)


@bp.route('/')
def start():
    """Show the experiment start page."""
    return 'starting the experiment'
