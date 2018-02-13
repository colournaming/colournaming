"""Views for the namer."""

from flask import Blueprint, jsonify, abort, request, current_app, render_template
from sqlalchemy.orm.exc import NoResultFound
from ..database import db
from .model import Language, NameAgreement
from .forms import NameAgreementForm
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

@bp.route('/lang/default/name')
def name_colour_default_lang():
    lang = request.accept_languages[0][0]
    if '-' in lang:
        # e.g. if lang = en-GB
        lang = lang.split('-')[0]
    return name_colour(lang)

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
        print('No namer available for', lang_code)
        abort(404)
    colours = namer.colour_name([red, green, blue])
    return jsonify(
        colours=colours,
        desc=render_template('match_description.html', colours=colours)
    )


@bp.route('/submit_agreement', methods=['POST'])
def submit_agreement():
    form = NameAgreementForm()
    print(
        form.csrf_token,
        form.language_code,
        form.red,
        form.green,
        form.blue,
        form.agreement
    )
    if form.validate_on_submit():
        print('name agreeement form is valid')
        lang = Language.query.filter(Language.code == form.language_code.data).one()
        agreement = NameAgreement(
            language=lang,
            red=form.red.data,
            green=form.green.data,
            blue=form.blue.data,
            agreement=form.agreement.data
        )
        db.session.add(agreement)
        db.session.commit()
        return jsonify(success=True)
    else:
        if form.errors:
            for field, error in form.errors.items():
                print(field, error)
        return jsonify(success=False)


@bp.route('/audiolist')
def audio_list():
    """Get available audio for a language."""
    lang = request.args.get('lang', 'en')
    return jsonify(controller.audio_list(lang))


@bp.route('/interface')
def interface():
    """Show the colour namer interface."""
    if request.mobile:
        template = 'namer-mobile.html'
    else:
        template = 'namer.html'
    return render_template(template, languages=controller.language_list())
