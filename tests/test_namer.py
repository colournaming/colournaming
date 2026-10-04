import io
import math

import numpy as np
import pytest
from flask import current_app, session
from flask_wtf.csrf import generate_csrf

from colournaming.database import db
from colournaming.namer import controller
from colournaming.namer.controller import ColourNamer
from colournaming.namer.model import AgreementLevel, ColourCentroid, Language, NameAgreement

# --- colour maths -------------------------------------------------------------------------------


@pytest.mark.parametrize(
    "component, expected",
    [(0, 0.0), (10, 10 / 255 / 12.92), (255, 1.0), (128, 0.2158605)],
)
def test_scale_component(component, expected):
    assert ColourNamer.scale_component(component) == pytest.approx(expected, rel=1e-5)


def test_srgb2xyz_white_is_d65():
    assert ColourNamer.srgb2xyz([255, 255, 255]) == pytest.approx([95.05, 100.0, 108.9], abs=0.01)


def test_xyz2lab():
    white = [95.04, 100.0, 108.89]
    assert ColourNamer.xyz2lab(white, white) == pytest.approx([100.0, 0.0, 0.0], abs=1e-4)
    assert ColourNamer.xyz2lab([0.0, 0.0, 0.0], white) == pytest.approx([0.0, 0.0, 0.0])
    red = ColourNamer.xyz2lab(ColourNamer.srgb2xyz([255, 0, 0]), white)
    assert red == pytest.approx([53.24, 80.09, 67.20], abs=0.05)


def test_euclidean_distance_ignores_lightness():
    assert ColourNamer.euclidean_distance([0, 0, 0], [100, 3, 4]) == pytest.approx(5.0)


def test_calculate_angle():
    assert ColourNamer.calculate_angle([0, 0, 0], [0, 2, 4]) == pytest.approx(0.5)
    with np.errstate(invalid="ignore"):
        assert ColourNamer.calculate_angle([0, 0, 0], np.array([0.0, 0.0, 0.0])) == 0.0


def test_mvnpdf_standard_normal():
    x = np.zeros(3)
    assert ColourNamer.mvnpdf(x, np.zeros(3), np.eye(3)) == pytest.approx((2 * math.pi) ** -1.5)
    x = np.array([1.0, 0.0, 0.0])
    expected = (2 * math.pi) ** -1.5 * math.exp(-0.5)
    assert ColourNamer.mvnpdf(x, np.zeros(3), np.eye(3)) == pytest.approx(expected)


# --- database backed controller functions -------------------------------------------------------


def test_read_centroids_from_file(english):
    lang = Language.query.filter(Language.code == "en").one()
    assert lang.name == "English"
    assert ColourCentroid.query.filter(ColourCentroid.language == lang).count() == 30
    assert isinstance(english, ColourNamer)


def test_read_centroids_reuses_existing_language(english):
    row = (
        "color_name,m_L,m_a,m_b,sigma_1,sigma_2,sigma_3,sigma_4,sigma_5,sigma_6,sigma_7,"
        "sigma_8,sigma_9,den,prob,m_R,m_G,m_B,exp\n"
        "octarine,50,-20,-5,100,0,0,0,100,0,0,0,100,0.001,0.01,0,128,128,1\n"
    )
    controller.read_centroids_from_file(io.StringIO(row), "Ignored", "en")
    assert Language.query.count() == 1
    assert ColourCentroid.query.filter(ColourCentroid.color_name == "octarine").count() == 1
    assert "octarine" in [d["colour_name"] for d in current_app.namers["en"].data]


@pytest.mark.parametrize(
    "rgb, expected",
    [
        ([255, 0, 0], "red"),
        ([0, 0, 255], "blue"),
        ([0, 160, 0], "green"),
        ([0, 0, 0], "black"),
        ([255, 255, 255], "white"),
        ([255, 255, 0], "yellow"),
    ],
)
def test_colour_name_top_match(english, rgb, expected):
    names = english.colour_name(rgb)
    assert names[0]["name"] == expected


def test_colour_name_result_structure(english):
    names = english.colour_name([200, 30, 30])
    assert len(names) == 4
    assert names[0]["d"] == 0
    likelihoods = [n["likelihood"] for n in names]
    assert likelihoods == sorted(likelihoods, reverse=True)
    assert set(names[0]) == {"name", "a", "b", "d", "likelihood", "red", "green", "blue"}


def test_colour_name_ignores_tiny_densities(english):
    for c in english.data:
        c["den"] = 0.0
    names = english.colour_name([255, 0, 0])
    assert all(n["likelihood"] == 0.0 for n in names)


def test_load_data_unknown_language():
    with pytest.raises(Exception):
        ColourNamer("xx")


def test_language_list(english):
    db.session.add(Language(name="French", code="fr"))
    db.session.commit()
    assert sorted(controller.language_list(), key=lambda x: x["code"]) == [
        {"name": "English", "code": "en"},
        {"name": "French", "code": "fr"},
    ]


def test_colour_list(english):
    lang = Language.query.filter(Language.code == "en").one()
    colours = {c["code"]: c for c in controller.colour_list(lang)}
    assert colours["red"]["name"] == "Red"
    assert colours["red"]["hex"] == "bd3e39"
    assert colours["light_blue"]["name"] == "Light blue"


def test_hex_code_for_colour_zero_pads():
    colour = ColourCentroid(m_R=5, m_G=0, m_B=255)
    assert controller._hex_code_for_colour(colour) == "0500ff"


def test_namer_hex_zero_pads():
    lang = Language(name="Test", code="tt")
    db.session.add(lang)
    db.session.add(
        ColourCentroid(
            language=lang,
            color_name="x",
            m_L=1,
            m_a=0,
            m_b=0,
            sigma_1=1,
            sigma_2=0,
            sigma_3=0,
            sigma_4=0,
            sigma_5=1,
            sigma_6=0,
            sigma_7=0,
            sigma_8=0,
            sigma_9=1,
            den=1,
            prob=1,
            m_R=5,
            m_G=0,
            m_B=255,
        )
    )
    db.session.commit()
    assert ColourNamer("tt").data[0]["hex"] == "0500ff"


def test_audio_list(app, tmp_path, monkeypatch):
    monkeypatch.setattr(app, "static_folder", str(tmp_path))
    (tmp_path / "audio" / "en").mkdir(parents=True)
    (tmp_path / "audio" / "en" / "red.mp3").write_bytes(b"")
    (tmp_path / "audio" / "en" / "notes.txt").write_bytes(b"")
    assert controller.audio_list("en") == ["red.mp3"]
    assert controller.audio_list("zz") is None


def test_instantiate_namers(english):
    namers = controller.instantiate_namers()
    assert list(namers) == ["en"]
    assert isinstance(namers["en"], ColourNamer)


# --- views --------------------------------------------------------------------------------------


def test_languages_view(client, english):
    assert client.get("/namer/lang/").get_json() == [{"name": "English", "code": "en"}]


def test_colours_view(client, english):
    rv = client.get("/namer/lang/en/colours")
    assert rv.status_code == 200
    assert len(rv.get_json()) == 30
    assert client.get("/namer/colours?lang=en").get_json() == rv.get_json()


def test_colours_view_unknown_language(client):
    assert client.get("/namer/lang/xx/colours").status_code == 404


@pytest.mark.parametrize("colour", ["red", "Red", "light_blue", "Light blue"])
def test_rgb_from_colour(client, english, colour):
    rv = client.get(f"/namer/lang/en/colours/{colour}")
    assert rv.status_code == 200
    assert rv.get_json()["code"] in ("red", "light_blue")


def test_rgb_from_colour_not_found(client, english):
    assert client.get("/namer/lang/en/colours/octarine").status_code == 404
    assert client.get("/namer/lang/xx/colours/red").status_code == 404


def test_name_colour_view(client, english):
    rv = client.get("/namer/lang/en/name?colour=ff0000")
    assert rv.status_code == 200
    data = rv.get_json()
    assert data["colours"][0]["name"] == "red"
    assert "desc" in data


@pytest.mark.parametrize("query", ["", "?colour=zzzzzz", "?colour=ff00"])
def test_name_colour_view_bad_colour(client, english, query):
    assert client.get(f"/namer/lang/en/name{query}").status_code == 500


def test_name_colour_view_unknown_language(client, english):
    assert client.get("/namer/lang/xx/name?colour=ff0000").status_code == 404


def test_name_colour_default_lang_from_header(client, english):
    rv = client.get("/namer/lang/default/name?colour=0000ff", headers={"Accept-Language": "en-GB"})
    assert rv.get_json()["colours"][0]["name"] == "blue"


def test_name_colour_default_lang_from_session(client, english):
    with client.session_transaction() as sess:
        sess["interface_language"] = "en"
    rv = client.get("/namer/lang/default/name?colour=0000ff", headers={"Accept-Language": "fr"})
    assert rv.status_code == 200


@pytest.fixture
def csrf_token(app, client, monkeypatch):
    """Enable CSRF protection and return a valid token for the client's session.

    submit_agreement reads form.csrf_token, which only exists when CSRF is enabled.
    """
    monkeypatch.setitem(app.config, "WTF_CSRF_ENABLED", True)
    with app.test_request_context():
        token = generate_csrf()
        raw = session["csrf_token"]
    with client.session_transaction() as sess:
        sess["csrf_token"] = raw
    return token


def test_submit_agreement(client, english, csrf_token):
    rv = client.post(
        "/namer/submit_agreement",
        data={
            "csrf_token": csrf_token,
            "language_code": "en",
            "red": "255",
            "green": "0",
            "blue": "0",
            "agreement": "agree",
        },
    )
    assert rv.get_json() == {"success": True}
    agreement = NameAgreement.query.one()
    assert agreement.language.code == "en"
    assert (agreement.red, agreement.green, agreement.blue) == (255, 0, 0)
    assert agreement.agreement == AgreementLevel.agree


def test_submit_agreement_invalid(client, english, csrf_token):
    rv = client.post(
        "/namer/submit_agreement", data={"csrf_token": csrf_token, "language_code": "english"}
    )
    assert rv.get_json() == {"success": False}
    assert NameAgreement.query.count() == 0


def test_audio_list_view(client, app, tmp_path, monkeypatch):
    monkeypatch.setattr(app, "static_folder", str(tmp_path))
    (tmp_path / "audio" / "en").mkdir(parents=True)
    (tmp_path / "audio" / "en" / "red.mp3").write_bytes(b"")
    assert client.get("/namer/audiolist").get_json() == ["red.mp3"]


@pytest.mark.parametrize(
    "user_agent, template_marker",
    [
        ("Mozilla/5.0 (X11; Linux x86_64) Firefox/120.0", "namer.html"),
        (
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 "
            "(KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
            "namer-mobile.html",
        ),
    ],
)
def test_interface_view(client, english, user_agent, template_marker, monkeypatch):
    import colournaming.namer.views as views

    rendered = []
    original = views.render_template

    def spy(template, **kwargs):
        rendered.append(template)
        return original(template, **kwargs)

    monkeypatch.setattr(views, "render_template", spy)
    rv = client.get("/namer/interface", headers={"User-Agent": user_agent})
    assert rv.status_code == 200
    assert rendered == [template_marker]
