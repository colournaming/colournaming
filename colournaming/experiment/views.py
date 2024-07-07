"""Views for the experiment."""

from datetime import datetime
from functools import wraps, update_wrapper
from flask import (
    Blueprint,
    View,
    abort,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
    make_response,
)
from flask_babel import lazy_gettext, get_locale
from . import controller, forms
from .. import lang_is_rtl
from ..utils import rgb2lab


def get_browser_language():
    try:
        browser_language = request.accept_languages[0][0]
    except IndexError:
        browser_language = None
    return browser_language


def set_common_session_values():

    
    
@bp.route("/fixed_background")
def start_fixed_background():
    """Show the experiment start page."""
    browser_language = get_browser_language()
    background_id, background_colour = -1, '#aaa'
    background_colour_lab = rgb2lab(background_colour)
    dark_font = background_colour_lab[0] > 80
    session["experiment"] = {
        "client": {
            "user_agent": request.user_agent.string,
            "browser_language": browser_language,
            "interface_language": session.get("interface_language", browser_language),
        },
        "response_count": 0,
        "background_id": background_id,
        "background_colour": background_colour,
        "dark_font": dark_font
    }
    return redirect(url_for(".display_properties"))

@bp.route
def start_colour_background():
    """Show the experiment start page."""
    print("resetting experiment")
    try:
        browser_language = request.accept_languages[0][0]
    except IndexError:
        browser_language = None
    try:
        background_id, background_colour = controller.get_random_background()
    except IndexError:
        abort(500, "No backgrounds have been imported")
    background_colour_lab = rgb2lab(background_colour)
    dark_font = background_colour_lab[0] > 80
    session["experiment"] = {
        "client": {
            "user_agent": request.user_agent.string,
            "browser_language": browser_language,
            "interface_language": session.get("interface_language", browser_language),
        },
        "response_count": 0,
        "background_id": background_id,
        "background_colour": background_colour,
        "dark_font": dark_font
    }
    return redirect(url_for("experimentcolbg.display_properties"))
