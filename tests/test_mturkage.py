"""Tests for the Prolific age study, which uses the foreground colour targets."""

import io

import pytest

from colournaming.database import db
from colournaming.experimentcol.model import ColourTarget
from colournaming.mturk.exceptions import MTurkIDNotFound
from colournaming.mturkage import controller
from colournaming.mturkage.model import MturkAgeColourResponse, MturkAgeParticipant, MturkAgeTask
from helpers import DISPLAY_FORM, OBSERVER_FORM

PROLIFIC_ARGS = "?PROLIFIC_PID=pid&STUDY_ID=study&SESSION_ID=sess"


def test_create_and_list_tasks():
    task = controller.create_mturk_task("pid", "study", "sess")
    assert controller.list_mturk_tasks() == [task]
    assert controller.get_mturk_task_by_id(task.id) == task


def test_get_mturk_task_by_id_not_found():
    with pytest.raises(MTurkIDNotFound):
        controller.get_mturk_task_by_id(999)


def test_get_random_target_returns_counted_target(col_targets):
    target = controller.get_random_target()
    assert target.presentation_count == 1


def test_read_targets_from_file(col_targets):
    controller.read_targets_from_file(
        io.StringIO("color_id,R,G,B\n9,1,2,3\n"), delete_existing=True
    )
    target = ColourTarget.query.one()
    assert (target.id, target.red, target.green, target.blue) == (9, 1, 2, 3)


def test_get_random_target_balances_presentations(col_targets):
    for _ in range(6):
        controller.get_random_target()
    assert sorted(t.presentation_count for t in ColourTarget.query.all()) == [2, 2, 2]


def test_save_participant_response_and_update(col_targets):
    task = controller.create_mturk_task("pid", "study", "sess")
    experiment = {
        "task_id": task.id,
        "client": {"browser_language": "en", "interface_language": "en", "user_agent": "ua"},
        "display": {
            "greyscale_levels": 3,
            "screen_width": 800,
            "screen_height": 600,
            "screen_colour_depth": 32,
        },
    }
    experiment["participant_id"] = controller.save_participant(experiment)
    count = controller.save_response(
        experiment, {"target_id": 1, "name": "red", "response_time": 1.0}
    )
    assert count == 1
    assert controller.response_count_percentage(count) == pytest.approx(100 / 3)
    experiment["observer"] = {
        "age": 70,
        "gender": "male",
        "gender_other": "",
        "colour_experience": "advanced",
        "language_experience": "bilingual",
        "education_level": "",
        "country_raised": "",
        "country_resident": "",
        "ambient_light": "",
        "screen_light": "",
        "screen_temperature": "",
        "screen_distance": None,
        "device": "pad",
        "location": "",
    }
    experiment["vision"] = {"square_disappeared": True}
    controller.update_participant(experiment)
    participant = MturkAgeParticipant.query.one()
    assert participant.age == 70
    assert participant.task.prolific_id == "pid"


def test_start_requires_prolific_ids(client):
    assert client.get("/mturkage/start").status_code == 500
    assert MturkAgeTask.query.count() == 0


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
def test_pages_redirect_without_experiment(client, page):
    rv = client.get("/mturkage/{}".format(page))
    assert rv.status_code == 302
    assert rv.headers["Location"].endswith("/mturkage/start")


def test_start_uses_grey_background(client):
    rv = client.get(f"/mturkage/start{PROLIFIC_ARGS}")
    assert rv.headers["Location"].endswith("/mturkage/display_properties.html")
    with client.session_transaction() as sess:
        assert sess["experiment"]["background_colour"] == (128, 128, 128)
        assert sess["experiment"]["dark_font"] is False


def test_full_experiment(client, col_targets):
    client.get(f"/mturkage/start{PROLIFIC_ARGS}")
    for page in ["display_properties.html", "colour_vision.html", "name_colour.html"]:
        assert client.get(f"/mturkage/{page}").status_code == 200
    # get_random_colour opens its own transaction, so give it the fresh session a real request
    # would have rather than the one shared with this test's app context
    db.session.remove()
    assert client.get("/mturkage/get_target.json").get_json()["id"] in (1, 2, 3)

    client.post("/mturkage/display_properties.html", data=DISPLAY_FORM)
    rv = client.post("/mturkage/colour_vision.html", data={"square_disappeared": "yes"})
    assert rv.headers["Location"].endswith("/mturkage/name_colour.html")

    # PROLIFIC_AGE_RESPONSE_COUNT is 3 in the test config
    for n in (1, 2, 3):
        rv = client.post(
            "/mturkage/name_colour.html",
            data={"name": "x", "target_id": str(n), "response_time": "1"},
        )
    assert rv.headers["Location"].endswith("/mturkage/observer_information.html")
    assert MturkAgeColourResponse.query.count() == 3

    rv = client.post("/mturkage/observer_information.html", data=OBSERVER_FORM)
    assert rv.headers["Location"].endswith("/mturkage/thankyou.html")
    assert MturkAgeParticipant.query.one().colour_target_disappeared is True


@pytest.mark.parametrize(
    "configured, expected",
    [
        (None, b"app.prolific.co/submissions/complete?cc=C8MYG78Z"),
        ("https://example.com/done", b"https://example.com/done"),
    ],
)
def test_thankyou_completion_url(app, client, monkeypatch, configured, expected):
    if configured:
        monkeypatch.setitem(app.config, "PROLIFIC_AGE_COMPLETION_URL", configured)
    client.get(f"/mturkage/start{PROLIFIC_ARGS}")
    rv = client.get("/mturkage/thankyou.html")
    assert expected in rv.data


def test_invalid_forms_rerender(client):
    client.get(f"/mturkage/start{PROLIFIC_ARGS}")
    assert client.post("/mturkage/display_properties.html", data={"levels": "x"}).status_code == 200
    assert (
        client.post(
            "/mturkage/colour_vision.html", data={"square_disappeared": "maybe"}
        ).status_code
        == 200
    )
    assert client.post("/mturkage/name_colour.html", data={}).status_code == 200
    assert client.post("/mturkage/observer_information.html", data={"age": "3"}).status_code == 200
