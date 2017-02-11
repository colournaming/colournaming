"""Views for the namer."""

from flask import Blueprint, jsonify, abort
from sqlalchemy.orm.exc import NoResultFound
from .model import ColourCentroid, Language

bp = Blueprint('namer', __name__)


@bp.route('/languages')
def languages():
    """List known languages."""
    languages = Language.query.all()
    language_list = [{'name': l.name, 'code': l.code} for l in languages]
    return jsonify(language_list)

@bp.route('/colours/<lang_code>')
def colours(lang_code):
    try:
        language = Language.query.filter(Language.code == lang_code).one()
    except NoResultFound:
        abort(404)
    colours = ColourCentroid.query.filter(ColourCentroid.language == language).all()
    colour_list = [c.color_name for c in colours]
    return jsonify(colour_list)