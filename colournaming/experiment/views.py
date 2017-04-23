"""Views for the experiment."""

from flask import Blueprint, jsonify, abort, request, current_app, render_template
from sqlalchemy.orm.exc import NoResultFound

bp = Blueprint('experiment', __name__)


@bp.route('/')
def start():
    """Show the experiment start page."""
    return 'starting the experiment'
