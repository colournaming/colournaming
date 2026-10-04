"""Tests for the Prolific (formerly Mechanical Turk) background colour experiment."""

import io

import pytest

from colournaming.database import db
from colournaming.experimentcolbg.model import BackgroundColour
from colournaming.mturk import controller
from colournaming.mturk.exceptions import MTurkIDNotFound
from colournaming.mturk.model import MturkColourResponseColBG, MturkParticipantColBG, MturkTask
from helpers import DISPLAY_FORM, OBSERVER_FORM

PROLIFIC_ARGS = "?PROLIFIC_PID=pid&STUDY_ID=study&SESSION_ID=sess"


# --- controller ---------------------------------------------------------------------------------


def test_get_random_colour_empty_table():
    with pytest.raises(IndexError):
        controller.get_random_colour(BackgroundColour)


def test_get_random_colour_increment(backgrounds):
    controller.get_random_colour(BackgroundColour)
    controller.get_random_colour(BackgroundColour)
    assert sorted(b.presentation_count for b in BackgroundColour.query.all()) == [1, 1]


def test_get_random_colour_no_increment(backgrounds):
    controller.get_random_colour(BackgroundColour, increment_presentation=False)
    assert [b.presentation_count for b in BackgroundColour.query.all()] == [0, 0]


def test_get_random_target_returns_counted_target(colbg_targets):
    target = controller.get_random_target()
    assert target.presentation_count == 1


def test_get_random_target_and_background(colbg_targets, backgrounds):
    assert controller.get_random_target().id in (1, 2, 3)
    bg_id, colour = controller.get_random_background()
    assert colour == {1: (250, 250, 250), 2: (20, 20, 20)}[bg_id]


def test_create_and_list_tasks():
    task = controller.create_mturk_task("pid", "study", "sess")
    assert (task.prolific_id, task.study_id, task.session_id) == ("pid", "study", "sess")
    assert controller.list_mturk_tasks() == [task]
    assert controller.get_mturk_task_by_id(task.id) == task


def test_get_mturk_task_by_id_not_found():
    with pytest.raises(MTurkIDNotFound):
        controller.get_mturk_task_by_id(999)


def test_read_targets_and_backgrounds():
    controller.read_targets_from_file(io.StringIO("color_id,R,G,B\n1,1,2,3\n"))
    controller.read_backgrounds_from_file(io.StringIO("bg_id,R,G,B\n1,4,5,6\n"))
    controller.read_targets_from_file(
        io.StringIO("color_id,R,G,B\n2,1,2,3\n"), delete_existing=True
    )
    controller.read_backgrounds_from_file(
        io.StringIO("bg_id,R,G,B\n2,4,5,6\n"), delete_existing=True
    )
    assert controller.get_random_target().id == 2
    assert controller.get_random_background() == (2, (4, 5, 6))


def test_save_participant_response_and_update(colbg_targets, backgrounds):
    task = controller.create_mturk_task("pid", "study", "sess")
    experiment = {
        "task_id": task.id,
        "background_id": 1,
        "client": {"browser_language": "en", "interface_language": "en", "user_agent": "ua"},
        "display": {
            "greyscale_levels": 3,
            "screen_width": 800,
            "screen_height": 600,
            "screen_colour_depth": 32,
        },
    }
    experiment["participant_id"] = controller.save_participant(experiment)
    assert controller.save_participant(experiment) == experiment["participant_id"]
    assert task.participant.id == experiment["participant_id"]

    for n in (1, 2):
        count = controller.save_response(
            experiment, {"target_id": n, "name": "x", "response_time": 1.0}
        )
        assert count == n
    assert controller.response_count_percentage(count) == pytest.approx(200 / 3)

    experiment["observer"] = {
        "age": 20,
        "gender": "other",
        "gender_other": "nb",
        "colour_experience": "",
        "language_experience": "",
        "education_level": "",
        "country_raised": "",
        "country_resident": "",
        "ambient_light": "",
        "screen_light": "",
        "screen_temperature": "",
        "screen_distance": None,
        "device": "",
        "location": "",
    }
    experiment["vision"] = {"square_disappeared": None}
    controller.update_participant(experiment)
    participant = MturkParticipantColBG.query.one()
    assert participant.gender_other == "nb"
    assert db.session.get(BackgroundColour, 1).presentation_count == 1


# --- views --------------------------------------------------------------------------------------


@pytest.mark.parametrize(
    "args", ["", "?PROLIFIC_PID=pid", "?PROLIFIC_PID=pid&STUDY_ID=study&SESSION_ID="]
)
def test_start_requires_prolific_ids(client, backgrounds, args):
    assert client.get(f"/mturk/{args}").status_code == 500
    assert MturkTask.query.count() == 0


def test_start_without_backgrounds(client):
    assert client.get(f"/mturk/{PROLIFIC_ARGS}").status_code == 500


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
    rv = client.get("/mturk/{}".format(page))
    assert rv.status_code == 302
    assert rv.headers["Location"].endswith("/mturk/")


def test_start_creates_task(client, backgrounds):
    rv = client.get(f"/mturk/{PROLIFIC_ARGS}")
    assert rv.headers["Location"].endswith("/mturk/display_properties.html")
    task = MturkTask.query.one()
    assert task.prolific_id == "pid"
    with client.session_transaction() as sess:
        assert sess["experiment"]["task_id"] == task.id


@pytest.mark.parametrize("answer, expected", [("yes", True), ("no", False), ("-", None)])
def test_colour_vision_answers(client, backgrounds, answer, expected):
    client.get(f"/mturk/{PROLIFIC_ARGS}")
    rv = client.post("/mturk/colour_vision.html", data={"square_disappeared": answer})
    assert rv.headers["Location"].endswith("/mturk/name_colour.html")
    with client.session_transaction() as sess:
        assert sess["experiment"]["vision"]["square_disappeared"] is expected


def test_full_experiment(client, colbg_targets, backgrounds):
    client.get(f"/mturk/{PROLIFIC_ARGS}")
    for page in ["display_properties.html", "colour_vision.html", "name_colour.html"]:
        assert client.get(f"/mturk/{page}").status_code == 200
    assert client.get("/mturk/get_target.json").status_code == 200

    client.post("/mturk/display_properties.html", data=DISPLAY_FORM)
    client.post("/mturk/colour_vision.html", data={"square_disappeared": "no"})

    # MTURK_RESPONSE_COUNT is 3 in the test config
    for n in (1, 2):
        rv = client.post(
            "/mturk/name_colour.html",
            data={"name": "x", "target_id": str(n), "response_time": "1"},
        )
        assert rv.status_code == 200
    rv = client.post(
        "/mturk/name_colour.html", data={"name": "x", "target_id": "3", "response_time": "1"}
    )
    assert rv.headers["Location"].endswith("/mturk/observer_information.html")
    assert MturkColourResponseColBG.query.count() == 3

    assert client.get("/mturk/observer_information.html").status_code == 200
    rv = client.post("/mturk/observer_information.html", data=OBSERVER_FORM)
    assert rv.headers["Location"].endswith("/mturk/thankyou.html")

    rv = client.get("/mturk/thankyou.html")
    assert b"100%" in rv.data
    assert b"app.prolific.co/submissions/complete" in rv.data


def test_invalid_forms_rerender(client, backgrounds):
    client.get(f"/mturk/{PROLIFIC_ARGS}")
    assert client.post("/mturk/display_properties.html", data={"levels": "x"}).status_code == 200
    assert (
        client.post("/mturk/colour_vision.html", data={"square_disappeared": "maybe"}).status_code
        == 200
    )
    assert client.post("/mturk/name_colour.html", data={}).status_code == 200
    assert client.post("/mturk/observer_information.html", data={"age": "3"}).status_code == 200


def test_get_target_without_targets(client):
    assert client.get("/mturk/get_target.json").status_code == 500


def test_thankyou_without_targets(client, backgrounds):
    client.get(f"/mturk/{PROLIFIC_ARGS}")
    assert client.get("/mturk/thankyou.html").status_code == 200
