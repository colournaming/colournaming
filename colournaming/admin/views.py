"""Views for the namer."""

from flask import (
    Blueprint,
    current_app,
    redirect,
    render_template,
    Response,
    session,
    url_for,
)
from .controller import (
    get_agreements,
    get_responses,
    get_participants,
    get_colbg_responses,
    get_colbg_participants,
    get_mturk_responses,
    get_mturk_participants,
)
from .forms import LoginForm

bp = Blueprint("admin", __name__)


@bp.route("/login", methods=["GET", "POST"])
def login():
    """Admin login page."""
    form = LoginForm()
    if form.validate_on_submit():
        admin_password = current_app.config.get("ADMIN_PASSWORD")
        if form.username.data == "admin" and form.password.data == admin_password:
            session["admin_logged_in"] = True
            return redirect(url_for(".index"))
    if form.errors:
        for field, error in form.errors.items():
            print(field, error)
    return render_template("login.html", form=form)


@bp.route("/")
def index():
    """Menu of admin functions."""
    if not session.get("admin_logged_in", False):
        return redirect(url_for(".login"))
    return render_template("admin_menu.html")


@bp.route("/responses.csv")
def show_responses():
    """Return experiment responses as CSV."""
    if not session.get("admin_logged_in", False):
        return redirect(url_for(".login"))
    f = io.StringIO()
    get_responses(f)
    return Response(f.read(), mimetype="text/csv")


@bp.route("/participants.csv")
def show_participants():
    """Return participants as CSV."""
    if not session.get("admin_logged_in", False):
        return redirect(url_for(".login"))
    return Response(get_participants(), mimetype="text/csv")


@bp.route("/agreements.csv")
def show_agreements():
    """Return agreements as CSV."""
    if not session.get("admin_logged_in", False):
        return redirect(url_for(".login"))
    return Response(get_agreements(), mimetype="text/csv")


@bp.route("/colbg_responses.csv")
def show_colbg_responses():
    """Return colour background experiment responses as CSV."""
    if not session.get("admin_logged_in", False):
        return redirect(url_for(".login"))
    return Response(get_colbg_responses(), mimetype="text/csv")


@bp.route("/colbg_participants.csv")
def show_colbg_participants():
    """Return colour background participants as CSV."""
    if not session.get("admin_logged_in", False):
        return redirect(url_for(".login"))
    return Response(get_colbg_participants(), mimetype="text/csv")


@bp.route("/mturk_responses.csv")
def show_mturk_responses():
    """Return Mechanical Turk experiment responses as CSV."""
    if not session.get("admin_logged_in", False):
        return redirect(url_for(".login"))
    return Response(get_mturk_responses(), mimetype="text/csv")


@bp.route("/mturk_participants.csv")
def show_mturk_participants():
    """Return Mechanical Turk participants as CSV."""
    if not session.get("admin_logged_in", False):
        return redirect(url_for(".login"))
    return Response(get_mturk_participants(), mimetype="text/csv")
