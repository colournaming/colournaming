"""Views for the namer."""

from flask import Blueprint, jsonify, abort, request, current_app, render_template
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
    """List colours known for a language."""
    try:
        lang = Language.query.filter(Language.code == lang_code).one()
    except NoResultFound:
        abort(404)
    return jsonify(controller.colour_list(lang))


@bp.route('/colours')
def get_colours():
    return colours(request.args.get('lang'))


@bp.route('/lang/<lang_code>/name')
def name_colour(lang_code):
    """Get nearest colour names for an RGB combination."""
    try:
        hexcode = request.args['colour']
        red = int(hexcode[0:2], 16)
        green = int(hexcode[2:4], 16)
        blue = int(hexcode[4:6], 16)
    except KeyError:
        abort(500)
    try:
        namer = current_app.namers[lang_code]
    except KeyError:
        abort(404)
    return jsonify(namer.colour_name([red, green, blue]))


@bp.route('/interface')
def interface():
    """Show the colour namer interface."""
    return render_template('namer.html', languages=controller.language_list())
