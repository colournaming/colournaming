"""Views for the front page."""

from flask import (
    Blueprint,
    current_app,
    render_template,
    request,
    session,
    redirect,
    url_for,
)
from flask_babel import get_locale
from flask_mail import Message
from .. import lang_is_rtl
from ..email import mail
from .forms import ContactForm
from ..namer import controller as namer_controller
from ..namer.forms import NameAgreementForm

bp = Blueprint("home", __name__)


@bp.route("/", methods=["GET", "POST"])
def index():
    """Render the front page."""
    contact_form = ContactForm()
    name_agreement_form = NameAgreementForm()
    if contact_form.validate_on_submit():
        msg = Message(
            "ColourNamer message from {0} {1}".format(
                contact_form.first_name.data, contact_form.last_name.data
            ),
            sender="contact@colornaming.net",
            recipients=[current_app.config["CONTACT_EMAIL"]],
        )
        msg_text = "FROM: {0} {1} <{2}>\nORGANISATION: {3}\n\n{4}".format(
            contact_form.first_name.data,
            contact_form.last_name.data,
            contact_form.email.data,
            contact_form.organisation.data,
            contact_form.message.data,
        )
        msg.body = msg_text
        mail.send(msg)
    try:
        current_language = request.accept_languages[0][0].split("-")[0]
    except IndexError:
        current_language = "en"

    return render_template(
        "index.html",
        contact_form=contact_form,
        name_agreement_form=name_agreement_form,
        languages=namer_controller.language_list(),
        interface_languages=current_app.config["LANGUAGES"],
        interface_language=session.get("interface_language", "en"),
        current_language=current_language,
        rtl=lang_is_rtl(get_locale()),
    )


@bp.route("lang/<lang>")
def set_language(lang):
    if lang:
        session["interface_language"] = lang
    print(lang)
    print(session["interface_language"])
    return redirect(url_for("home.index"))


@bp.route("interface_language")
def interface_language():
    lang = request.args.get("lang", None)
    if lang:
        session["interface_language"] = lang
    print(lang)
    print(session["interface_language"])
    return redirect(url_for("home.index"))
