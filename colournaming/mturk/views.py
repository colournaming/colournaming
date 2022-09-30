"""Views for the experiment."""

from datetime import datetime
from functools import wraps, update_wrapper
from flask import (
    abort,
    Blueprint,
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

bp = Blueprint("mturk", __name__)


def check_in_experiment():
    """Redirect to the start of the experiment if the session is not initialized."""
    if "experiment" not in session:
        return redirect(url_for("mturk.start"))


def rgb_tuple_to_css_rgb(background):
    return "rgb({0}, {1}, {2})".format(*background)


def nocache(view):
    @wraps(view)
    def func(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers["Last-Modified"] = datetime.now()
        response.headers[
            "Cache-Control"
        ] = "no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "-1"
        return response

    return update_wrapper(func, view)


@bp.route("/")
def start():
    """Show the experiment start page."""
    try:
        browser_language = request.accept_languages[0][0]
    except IndexError:
        browser_language = None
    try:
        background_id, background_colour = controller.get_random_background()
    except IndexError:
        abort(500, "No backgrounds have been imported")
    mturk_task = controller.create_mturk_task()
    session["experiment"] = {
        "client": {
            "user_agent": request.user_agent.string,
            "browser_language": browser_language,
            "interface_language": session.get("interface_language", browser_language),
        },
        "task_id": mturk_task.task_id,
        "response_count": 0,
        "background_id": background_id,
        "background_colour": background_colour,
    }
    return redirect(url_for("mturk.display_properties"))


@bp.route("/display_properties.html", methods=["GET", "POST"])
def display_properties():
    """Show the display properties form and handle responses."""
    check_in_experiment()
    form = forms.DisplayForm()
    if form.validate_on_submit():
        session["experiment"]["display"] = {
            "greyscale_levels": form.levels.data,
            "screen_width": form.screen_width.data,
            "screen_height": form.screen_height.data,
            "screen_colour_depth": form.screen_colour_depth.data,
        }
        session["experiment"]["participant_id"] = controller.save_participant(session["experiment"])
        session.modified = True
        return redirect(url_for("mturk.colour_vision"))
    if form.errors:
        for field, error in form.errors.items():
            print(field, error)
    return render_template(
        "display_properties.html",
        background_colour=rgb_tuple_to_css_rgb(session["experiment"]["background_colour"]),
        rtl=lang_is_rtl(get_locale()),
        form=form,
    )


@bp.route("/colour_vision.html", methods=["GET", "POST"])
def colour_vision():
    """Show the colour vision test and handle responses."""
    check_in_experiment()
    form = forms.ColourVisionForm()
    if form.validate_on_submit():
        print("colour vision form validated")
        session["experiment"]["vision"] = {"square_disappeared": form.square_disappeared.data}
        session.modified = True
        print(session)
        return redirect(url_for("mturk.name_colour"))
    if form.errors:
        for field, error in form.errors.items():
            print(field, error)
    return render_template(
        "colour_vision.html",
        background_colour=rgb_tuple_to_css_rgb(session["experiment"]["background_colour"]),
        form=form,
        rtl=lang_is_rtl(get_locale()),
    )


@bp.route("/name_colour.html", methods=["GET", "POST"])
def name_colour():
    """Show the name colour form and handle responses."""
    check_in_experiment()
    form = forms.ColourNameForm()
    if form.validate_on_submit():
        controller.save_response(
            session["experiment"],
            {
                "target_id": form.target_id.data,
                "name": form.name.data,
                "response_time": form.response_time.data,
            },
        )
        session["experiment"]["response_count"] += 1
        session.modified = True
        print("session:", session["experiment"])
        if session["experiment"]["response_count"] >= 10:
            print("redirecting to observer information", session["experiment"]["response_count"])
            return redirect(url_for("mturk.observer_information"))
        else:
            print("not redirecting", session["experiment"]["response_count"])
    if form.errors:
        for field, error in form.errors.items():
            print(field, error)
    return render_template(
        "name_colour.html",
        get_target_url=url_for("mturk.get_target"),
        background_colour=rgb_tuple_to_css_rgb(session["experiment"]["background_colour"]),
        form=form,
        rtl=lang_is_rtl(get_locale()),
    )


@bp.route("/get_target.json")
@nocache
def get_target():
    """Get a random colour target to name."""
    try:
        target = controller.get_random_target()
    except IndexError:
        abort(500, "No targets have been imported")
    return jsonify({"id": target.id, "r": target.red, "g": target.green, "b": target.blue})


@bp.route("/observer_information.html", methods=["GET", "POST"])
def observer_information():
    """Show the observer information form and handle responses."""
    check_in_experiment()
    form = forms.ObserverInformationForm()
    if form.validate_on_submit():
        print("observer information form validated")
        session["experiment"]["observer"] = {
            "age": form.age.data,
            "gender": form.gender.data,
            "gender_other": form.gender_other.data,
            "colour_experience": form.colour_experience.data,
            "language_experience": form.language_experience.data,
            "education_level": form.education_level.data,
            "country_raised": form.country_raised.data,
            "country_resident": form.country_resident.data,
            "ambient_light": form.ambient_light.data,
            "screen_light": form.screen_light.data,
            "screen_temperature": form.screen_temperature.data,
            "screen_distance": form.screen_distance.data,
            "device": form.display_device.data,
            "location": form.location.data,
        }
        session.modified = True
        controller.update_participant(session["experiment"])
        return redirect(url_for("mturk.thankyou"))
    if form.errors:
        for field, error in form.errors.items():
            print(field, repr(getattr(form, field).data), error)
    return render_template(
        "observer_information.html",
        form=form,
        background_colour=rgb_tuple_to_css_rgb(session["experiment"]["background_colour"]),
        rtl=lang_is_rtl(get_locale()),
    )


@bp.route("/thankyou.html")
def thankyou():
    """Show the thankyou for participation page."""
    try:
        response_count = session["experiment"].get("response_count", 0)
        perc = controller.response_count_percentage(response_count)
    except Exception:
        perc = 0
    top_namers_msg = lazy_gettext("You are in the 0% top colour namers.")
    top_namers_msg = top_namers_msg.replace("0%", "{0:.0f}%".format(perc))
    return render_template(
        "thankyou.html",
        mturk_completion=controller.get_mturk_task_by_id(
            session["experiment"]["task_id"]
        ).completion_id,
        top_namers=top_namers_msg,
        background_colour=rgb_tuple_to_css_rgb(session["experiment"]["background_colour"]),
        rtl=lang_is_rtl(get_locale()),
    )
