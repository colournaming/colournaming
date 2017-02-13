"""Views for the namer."""

from flask import Blueprint, jsonify, abort, request, current_app
from sqlalchemy.orm.exc import NoResultFound
from .model import Language
from . import controller

bp = Blueprint('namer', __name__)


@bp.route('/lang/')
def languages():
    """List known languages."""
    return jsonify(controller.language_list())


@bp.route('/lang/<lang_code>/colours')
def colours(lang_code):
    try:
        Language.query.filter(Language.code == lang_code).one()
    except NoResultFound:
        abort(404)
    return jsonify(controller.colour_list(lang_code))


@bp.route('/lang/<lang_code>/name')
def name_colour(lang_code):
    try:
        r = int(request.args['r'])
        g = int(request.args['g'])
        b = int(request.args['b'])
    except KeyError:
        abort(500)
    try:
        namer = current_app.namers[lang_code]
    except KeyError:
        abort(404)
    return jsonify(namer.colour_name([r, g, b]))
