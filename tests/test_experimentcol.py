import io

import pytest

from colournaming.database import AmbientLight, Device, Gender, db
from colournaming.experimentcol import controller
from colournaming.experimentcol.model import ColourResponse, ColourTarget, Participant
from helpers import DISPLAY_FORM, OBSERVER_FORM


def make_experiment():
    return {
        "client": {"browser_language": "en-GB", "interface_language": "en", "user_agent": "ua"},
        "display": {
            "greyscale_levels": 10,
            "screen_width": 1920,
            "screen_height": 1080,
            "screen_colour_depth": 24,
        },
    }


def observer_data(**overrides):
    observer = {
        "age": 35,
        "gender": "female",
        "gender_other": "",
        "colour_experience": "beginner",
        "language_experience": "native_speaker",
        "education_level": "doctorate_degree",
        "country_raised": "GB",
        "country_resident": "",
        "ambient_light": "dark",
        "screen_light": "dim",
        "screen_temperature": "warm_white",
        "screen_distance": 50.0,
        "device": "desktop",
        "location": "",
    }
    observer.update(overrides)
    return observer


# --- controller ---------------------------------------------------------------------------------


def test_read_targets_from_file():
    controller.read_targets_from_file(io.StringIO("id,red,green,blue\n7,1,2,3\n8,4,5,6\n"))
    targets = ColourTarget.query.order_by(ColourTarget.id).all()
    assert [(t.id, t.red, t.green, t.blue) for t in targets] == [(7, 1, 2, 3), (8, 4, 5, 6)]
    assert all(t.presentation_count == 0 for t in targets)


def test_get_random_target_no_targets():
    with pytest.raises(IndexError):
        controller.get_random_target()


def test_get_random_target_balances_presentations(col_targets):
    for _ in range(9):
        controller.get_random_target()
    assert sorted(t.presentation_count for t in ColourTarget.query.all()) == [3, 3, 3]


def test_get_random_target_prefers_least_presented(col_targets):
    col_targets[0].presentation_count = 5
    col_targets[1].presentation_count = 5
    controller.db.session.commit()
    assert controller.get_random_target().id == 3


def test_get_random_target_returns_counted_target(col_targets, monkeypatch):
    choices = iter([col_targets[0], col_targets[1]])
    monkeypatch.setattr(controller.random, "choice", lambda seq: next(choices))
    target = controller.get_random_target()
    assert target.presentation_count == 1


def test_response_count_percentage(col_targets):
    assert controller.response_count_percentage(0) == 0.0
    assert controller.response_count_percentage(3) == pytest.approx(100.0)
    assert controller.response_count_percentage(1) == pytest.approx(100 / 3)


def test_save_participant_creates_record():
    participant_id = controller.save_participant(make_experiment())
    p = db.session.get(Participant, participant_id)
    assert p.browser_language == "en-GB"
    assert p.interface_language == "en"
    assert p.user_agent == "ua"
    assert (p.greyscale_steps, p.screen_resolution_w, p.screen_resolution_h) == (10, 1920, 1080)
    assert p.screen_colour_depth == 24


def test_save_participant_existing_id_is_reused():
    experiment = make_experiment()
    experiment["participant_id"] = 42
    assert controller.save_participant(experiment) == 42
    assert Participant.query.count() == 0


def test_save_response(col_targets):
    experiment = make_experiment()
    experiment["participant_id"] = controller.save_participant(experiment)
    controller.save_response(experiment, {"target_id": 2, "name": "green", "response_time": 1.5})
    response = ColourResponse.query.one()
    assert response.participant.id == experiment["participant_id"]
    assert response.target.green == 255
    assert response.name == "green"
    assert response.response_time == 1.5


def test_update_participant():
    experiment = make_experiment()
    experiment["participant_id"] = controller.save_participant(experiment)
    experiment["observer"] = observer_data()
    experiment["vision"] = {"square_disappeared": True}
    controller.update_participant(experiment)
    p = db.session.get(Participant, experiment["participant_id"])
    assert p.age == 35
    assert p.gender == Gender.female
    assert p.ambient_light == AmbientLight.dark
    assert p.device == Device.desktop
    assert p.country_raised == "GB"
    assert p.country_resident is None
    assert p.gender_other is None
    assert p.colour_target_disappeared is True


# --- views --------------------------------------------------------------------------------------


def test_start_initialises_session(client):
    rv = client.get(
        "/experimentcol/", headers={"Accept-Language": "fr", "User-Agent": "test-agent"}
    )
    assert rv.status_code == 302
    assert rv.headers["Location"].endswith("/experimentcol/display_properties.html")
    with client.session_transaction() as sess:
        assert sess["experiment"] == {
            "client": {
                "user_agent": "test-agent",
                "browser_language": "fr",
                "interface_language": "fr",
            },
            "response_count": 0,
        }


def test_start_uses_interface_language_from_session(client):
    with client.session_transaction() as sess:
        sess["interface_language"] = "fa"
    client.get("/experimentcol/")
    with client.session_transaction() as sess:
        assert sess["experiment"]["client"]["browser_language"] is None
        assert sess["experiment"]["client"]["interface_language"] == "fa"


@pytest.mark.parametrize(
    "page",
    [
        "display_properties.html",
        "colour_vision.html",
        "name_colour.html",
        "observer_information.html",
        "thankyou.html",
    ],
)
def test_pages_render(client, page):
    client.get("/experimentcol/")
    rv = client.get(f"/experimentcol/{page}")
    assert rv.status_code == 200


@pytest.mark.parametrize(
    "page",
    [
        "display_properties.html",
        "colour_vision.html",
        "name_colour.html",
        "observer_information.html",
    ],
)
def test_pages_redirect_without_experiment(client, page):
    rv = client.get("/experimentcol/{}".format(page))
    assert rv.status_code == 302
    assert rv.headers["Location"].endswith("/experimentcol/")


def test_get_target(client, col_targets):
    rv = client.get("/experimentcol/get_target.json")
    assert rv.status_code == 200
    assert rv.headers["Pragma"] == "no-cache"
    assert "no-store" in rv.headers["Cache-Control"]
    data = rv.get_json()
    assert set(data) == {"id", "r", "g", "b"}
    assert data["id"] in (1, 2, 3)


def test_get_target_without_targets(client):
    assert client.get("/experimentcol/get_target.json").status_code == 500


def test_invalid_forms_rerender(client):
    client.get("/experimentcol/")
    rv = client.post("/experimentcol/display_properties.html", data={"levels": "99"})
    assert rv.status_code == 200
    rv = client.post("/experimentcol/name_colour.html", data={"name": ""})
    assert rv.status_code == 200
    assert ColourResponse.query.count() == 0
    rv = client.post("/experimentcol/observer_information.html", data={"age": "5"})
    assert rv.status_code == 200


def test_full_experiment(client, col_targets):
    client.get("/experimentcol/", headers={"Accept-Language": "en"})

    rv = client.post("/experimentcol/display_properties.html", data=DISPLAY_FORM)
    assert rv.headers["Location"].endswith("/experimentcol/colour_vision.html")
    participant = Participant.query.one()
    assert participant.screen_resolution_w == 1920

    rv = client.post("/experimentcol/colour_vision.html", data={"square_disappeared": "y"})
    assert rv.headers["Location"].endswith("/experimentcol/name_colour.html")

    for target_id, name in [(1, "red"), (2, "green")]:
        rv = client.post(
            "/experimentcol/name_colour.html",
            data={"name": name, "target_id": str(target_id), "response_time": "1.25"},
        )
        assert rv.status_code == 200
    responses = ColourResponse.query.order_by(ColourResponse.target_id).all()
    assert [(r.target_id, r.name) for r in responses] == [(1, "red"), (2, "green")]
    assert all(r.participant_id == participant.id for r in responses)

    rv = client.post("/experimentcol/observer_information.html", data=OBSERVER_FORM)
    assert rv.headers["Location"].endswith("/experimentcol/thankyou.html")
    controller.db.session.refresh(participant)
    assert participant.age == 35
    assert participant.country_resident == "FR"
    assert participant.colour_target_disappeared is True

    rv = client.get("/experimentcol/thankyou.html")
    assert b"67%" in rv.data


def test_thankyou_without_targets(client):
    client.get("/experimentcol/")
    with client.session_transaction() as sess:
        sess["experiment"]["response_count"] = 5
    rv = client.get("/experimentcol/thankyou.html")
    assert rv.status_code == 200
    assert b"0%" in rv.data
