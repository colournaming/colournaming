import io

import pytest

from colournaming.database import db
from colournaming.experimentcolbg import controller
from colournaming.experimentcolbg.model import (
    BackgroundColour,
    ColourResponseColBG,
    ColourTargetColBG,
    ParticipantColBG,
)
from colournaming.experimentcolbg.views import rgb_tuple_to_css_rgb
from helpers import DISPLAY_FORM, OBSERVER_FORM


def test_rgb_tuple_to_css_rgb():
    assert rgb_tuple_to_css_rgb((1, 2, 3)) == "rgb(1, 2, 3)"


# --- controller ---------------------------------------------------------------------------------


def test_read_targets_from_file(colbg_targets):
    controller.read_targets_from_file(io.StringIO("color_id,R,G,B\n9,1,2,3\n"))
    assert ColourTargetColBG.query.count() == 4


def test_read_targets_from_file_delete_existing(colbg_targets):
    controller.read_targets_from_file(
        io.StringIO("color_id,R,G,B\n9,1,2,3\n"), delete_existing=True
    )
    target = ColourTargetColBG.query.one()
    assert (target.id, target.red, target.green, target.blue) == (9, 1, 2, 3)


def test_read_backgrounds_from_file(backgrounds):
    controller.read_backgrounds_from_file(io.StringIO("bg_id,R,G,B,Label\n9,1,2,3,x\n"))
    assert BackgroundColour.query.count() == 3


def test_read_backgrounds_from_file_delete_existing(backgrounds):
    controller.read_backgrounds_from_file(
        io.StringIO("bg_id,R,G,B,Label\n9,1,2,3,x\n"), delete_existing=True
    )
    bg = BackgroundColour.query.one()
    assert (bg.id, bg.red, bg.green, bg.blue) == (9, 1, 2, 3)


def test_get_random_target_balances_presentations(colbg_targets):
    for _ in range(6):
        controller.get_random_target()
    assert sorted(t.presentation_count for t in ColourTargetColBG.query.all()) == [2, 2, 2]


def test_get_random_background(backgrounds):
    backgrounds[0].presentation_count = 3
    db.session.commit()
    assert controller.get_random_background() == (2, (20, 20, 20))
    # choosing a background does not count as a presentation
    assert BackgroundColour.query.get(2).presentation_count == 0


def test_response_count_percentage(colbg_targets):
    assert controller.response_count_percentage(3) == pytest.approx(100.0)


def make_experiment(background_id=1):
    return {
        "client": {"browser_language": "en", "interface_language": "en", "user_agent": "ua"},
        "display": {
            "greyscale_levels": 3,
            "screen_width": 800,
            "screen_height": 600,
            "screen_colour_depth": 32,
        },
        "background_id": background_id,
    }


def test_save_participant_and_response(colbg_targets, backgrounds):
    experiment = make_experiment()
    experiment["participant_id"] = controller.save_participant(experiment)
    assert controller.save_participant(experiment) == experiment["participant_id"]
    controller.save_response(experiment, {"target_id": 1, "name": "red", "response_time": 0.5})
    response = ColourResponseColBG.query.one()
    assert response.background.id == 1
    assert response.target.id == 1
    assert response.participant.screen_resolution_w == 800


def test_update_participant_counts_background(backgrounds):
    experiment = make_experiment(background_id=2)
    experiment["participant_id"] = controller.save_participant(experiment)
    experiment["observer"] = {
        k: ""
        for k in [
            "age",
            "gender",
            "gender_other",
            "colour_experience",
            "language_experience",
            "education_level",
            "country_raised",
            "country_resident",
            "ambient_light",
            "screen_light",
            "screen_temperature",
            "screen_distance",
            "device",
            "location",
        ]
    }
    experiment["observer"]["age"] = 40
    experiment["vision"] = {"square_disappeared": False}
    controller.update_participant(experiment)
    participant = ParticipantColBG.query.one()
    assert participant.age == 40
    assert participant.gender is None
    assert participant.colour_target_disappeared is False
    assert BackgroundColour.query.get(2).presentation_count == 1
    assert BackgroundColour.query.get(1).presentation_count == 0


# --- views --------------------------------------------------------------------------------------


@pytest.mark.xfail(strict=True, reason="max() of an empty table is None, giving ArgumentError")
def test_start_without_backgrounds(client):
    assert client.get("/experimentcolbg/").status_code == 500


@pytest.mark.parametrize("bg_id, dark_font", [(1, True), (2, False)])
def test_start_picks_font_colour(client, backgrounds, monkeypatch, bg_id, dark_font):
    bg = backgrounds[bg_id - 1]
    monkeypatch.setattr(
        controller, "get_random_background", lambda: (bg.id, (bg.red, bg.green, bg.blue))
    )
    rv = client.get("/experimentcolbg/")
    assert rv.headers["Location"].endswith("/experimentcolbg/display_properties.html")
    with client.session_transaction() as sess:
        assert sess["experiment"]["background_id"] == bg_id
        assert sess["experiment"]["dark_font"] is dark_font


def test_get_target(client, colbg_targets):
    rv = client.get("/experimentcolbg/get_target.json")
    assert rv.get_json()["id"] in (1, 2, 3)
    assert rv.headers["Expires"] == "-1"


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
def test_pages_render_with_background(client, backgrounds, page):
    client.get("/experimentcolbg/")
    with client.session_transaction() as sess:
        colour = sess["experiment"]["background_colour"]
    rv = client.get(f"/experimentcolbg/{page}")
    assert rv.status_code == 200
    assert rgb_tuple_to_css_rgb(colour).encode() in rv.data


def test_full_experiment(client, colbg_targets, backgrounds):
    client.get("/experimentcolbg/")
    with client.session_transaction() as sess:
        background_id = sess["experiment"]["background_id"]

    rv = client.post("/experimentcolbg/display_properties.html", data=DISPLAY_FORM)
    assert rv.headers["Location"].endswith("/experimentcolbg/colour_vision.html")
    rv = client.post("/experimentcolbg/colour_vision.html", data={})
    assert rv.headers["Location"].endswith("/experimentcolbg/name_colour.html")
    rv = client.post(
        "/experimentcolbg/name_colour.html",
        data={"name": "blue", "target_id": "3", "response_time": "2"},
    )
    assert rv.status_code == 200
    response = ColourResponseColBG.query.one()
    assert response.background_id == background_id
    assert response.name == "blue"

    rv = client.post("/experimentcolbg/observer_information.html", data=OBSERVER_FORM)
    assert rv.headers["Location"].endswith("/experimentcolbg/thankyou.html")
    participant = ParticipantColBG.query.one()
    assert participant.colour_target_disappeared is False
    assert BackgroundColour.query.get(background_id).presentation_count == 1

    rv = client.get("/experimentcolbg/thankyou.html")
    assert b"33%" in rv.data


def test_invalid_forms_rerender(client, backgrounds):
    client.get("/experimentcolbg/")
    assert (
        client.post("/experimentcolbg/display_properties.html", data={"levels": "x"}).status_code
        == 200
    )
    assert client.post("/experimentcolbg/name_colour.html", data={}).status_code == 200
    assert (
        client.post("/experimentcolbg/observer_information.html", data={"gender": "x"}).status_code
        == 200
    )
