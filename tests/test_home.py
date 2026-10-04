from types import SimpleNamespace

import pytest
from flask import request, session
from werkzeug.exceptions import Unauthorized

from colournaming import get_locale, lang_is_rtl
from colournaming.email import mail


def test_homepage(client, english):
    rv = client.get("/", headers={"Accept-Language": "en"})
    assert rv.status_code == 200
    assert b"Colour Naming" in rv.data


def test_homepage_without_accept_language(client):
    rv = client.get("/")
    assert rv.status_code == 200


def test_homepage_rtl_language(client):
    rv = client.get("/", headers={"Accept-Language": "fa"})
    assert rv.status_code == 200
    assert b"direction: rtl" in rv.data


def test_contact_form_sends_email(client):
    with mail.record_messages() as outbox:
        rv = client.post(
            "/",
            data={
                "first_name": "Ada",
                "last_name": "Lovelace",
                "email": "ada@example.com",
                "organisation": "Analytical Engines",
                "message": "Hello",
            },
        )
    assert rv.status_code == 200
    assert len(outbox) == 1
    msg = outbox[0]
    assert msg.subject == "ColourNamer message from Ada Lovelace"
    assert msg.recipients == ["contact@example.com"]
    assert "FROM: Ada Lovelace <ada@example.com>" in msg.body
    assert "ORGANISATION: Analytical Engines" in msg.body
    assert msg.body.endswith("Hello")


def test_homepage_get_sends_no_email(client):
    with mail.record_messages() as outbox:
        client.get("/")
    assert outbox == []


def test_robots(client):
    rv = client.get("/robots.txt")
    assert rv.status_code == 200
    assert rv.mimetype == "text/plain"
    rv.close()


def test_set_language(client):
    rv = client.get("/lang/fr")
    assert rv.status_code == 302
    assert rv.headers["Location"].endswith("/")
    with client.session_transaction() as sess:
        assert sess["interface_language"] == "fr"


def test_interface_language(client):
    rv = client.get("/interface_language?lang=fa")
    assert rv.status_code == 302
    with client.session_transaction() as sess:
        assert sess["interface_language"] == "fa"


def test_interface_language_keeps_existing_choice(client):
    with client.session_transaction() as sess:
        sess["interface_language"] = "en"
    rv = client.get("/interface_language")
    assert rv.status_code == 302
    with client.session_transaction() as sess:
        assert sess["interface_language"] == "en"


def test_not_found(client):
    rv = client.get("/does-not-exist")
    assert rv.status_code == 404


def test_permission_denied_handler(app):
    with app.test_request_context():
        rv = app.make_response(app.handle_user_exception(Unauthorized()))
    assert rv.status_code == 401


@pytest.mark.parametrize(
    "session_lang, header, expected",
    [
        (None, "fr", "fr"),
        (None, "de, fa;q=0.5", "fa"),
        ("fa", "fr", "fa"),
        ("xx", "fr", "fr"),
        (None, "de", None),
    ],
)
def test_get_locale(app, session_lang, header, expected):
    with app.test_request_context(headers={"Accept-Language": header}):
        if session_lang:
            session["interface_language"] = session_lang
        assert get_locale() == expected


@pytest.mark.parametrize(
    "language, expected",
    [("ar", True), ("fa", True), ("sd", True), ("he", True), ("en", False), ("fr", False)],
)
def test_lang_is_rtl(language, expected):
    assert lang_is_rtl(SimpleNamespace(language=language)) is expected


@pytest.mark.parametrize(
    "user_agent, mobile",
    [
        ("", False),
        ("Mozilla/5.0 (X11; Linux x86_64) Firefox/120.0", False),
        ("Mozilla/5.0 (Linux; Android 14; Pixel 8) Mobile Safari/537.36", True),
    ],
)
def test_before_request_detects_mobile(app, user_agent, mobile):
    with app.test_request_context(headers={"User-Agent": user_agent}):
        app.preprocess_request()
        assert request.mobile is mobile
