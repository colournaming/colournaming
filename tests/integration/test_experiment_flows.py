"""Run each experiment from start to finish in a browser and check what is stored."""

import re
from dataclasses import dataclass, field

import pytest
from playwright.sync_api import expect

from colournaming.database import db
from colournaming.experimentcol.model import ColourResponse, Participant
from colournaming.experimentcolbg.model import (
    BackgroundColour,
    ColourResponseColBG,
    ParticipantColBG,
)
from colournaming.mturk.model import MturkColourResponseColBG, MturkParticipantColBG, MturkTask
from colournaming.mturkage.model import MturkAgeColourResponse, MturkAgeParticipant, MturkAgeTask
from helpers import OBSERVER_FORM

COLOUR_NAMES = ["red", "sea green", "bleu foncé"]
GREYSCALE_LEVELS = 10
PROLIFIC_IDS = {"PROLIFIC_PID": "prolific-1", "STUDY_ID": "study-1", "SESSION_ID": "session-1"}
PROLIFIC_QUERY = "&".join(f"{k}={v}" for k, v in PROLIFIC_IDS.items())
PROLIFIC_COMPLETION_URL = "https://app.prolific.co/submissions/complete?cc=C8MYG78Z"

# Observer form fields stored as enums, keyed by form field with the participant column as value.
ENUM_FIELDS = {
    "gender": "gender",
    "colour_experience": "colour_experience",
    "language_experience": "language_experience",
    "education_level": "education_level",
    "display_device": "device",
    "screen_temperature": "screen_temperature",
    "screen_light": "screen_light",
    "ambient_light": "ambient_light",
}


@dataclass(frozen=True)
class Flow:
    """How to start an experiment and where its results are stored."""

    prefix: str
    participant_model: type
    response_model: type
    task_model: type | None = None
    start_path: str | None = None  # None for experiments started from the home page
    has_background: bool = False


FLOWS = {
    "experimentcol": Flow("/experimentcol", Participant, ColourResponse),
    "experimentcolbg": Flow(
        "/experimentcolbg", ParticipantColBG, ColourResponseColBG, has_background=True
    ),
    "mturk": Flow(
        "/mturk",
        MturkParticipantColBG,
        MturkColourResponseColBG,
        task_model=MturkTask,
        start_path=f"/mturk/?{PROLIFIC_QUERY}",
        has_background=True,
    ),
    "mturkage": Flow(
        "/mturkage",
        MturkAgeParticipant,
        MturkAgeColourResponse,
        task_model=MturkAgeTask,
        start_path=f"/mturkage/start?{PROLIFIC_QUERY}",
    ),
}

# Experiments where a "no" answer to the colour vision question is stored as True because
# ColourVisionForm.square_disappeared is a BooleanField, which only treats "false" and "" as False.
COLOUR_VISION_NO_BROKEN = {"experimentcol", "experimentcolbg"}


@dataclass
class Session:
    """What the browser saw and entered during an experiment."""

    screen: dict
    user_agent: str
    background_colour: str
    responses: list = field(default_factory=list)  # (target id, name) in the order given


def page_url(flow, name):
    return re.compile(re.escape(f"{flow.prefix}/{name}") + "$")


def is_name_colour_post(response):
    return response.request.method == "POST" and response.url.endswith("name_colour.html")


def run_experiment(page, flow, square_disappeared="yes"):
    """Complete every task of an experiment as a participant would."""
    if flow.start_path is None:
        page.goto("/")
        page.locator(f"a[href='{flow.prefix}/']").click()
    else:
        page.goto(flow.start_path)

    # Display properties task
    expect(page).to_have_url(page_url(flow, "display_properties.html"))
    session = Session(
        screen=page.evaluate(
            "({width: screen.width, height: screen.height, depth: screen.colorDepth})"
        ),
        user_agent=page.evaluate("navigator.userAgent"),
        background_colour=page.evaluate("getComputedStyle(document.body).backgroundColor"),
    )
    page.select_option("#levels", str(GREYSCALE_LEVELS))

    # Colour vision task
    expect(page).to_have_url(page_url(flow, "colour_vision.html"))
    page.select_option("#appearance", square_disappeared)

    # Colour naming task
    expect(page).to_have_url(page_url(flow, "name_colour.html"))
    colour_name = page.locator("#colour-name")
    colour_id = page.locator("#colour-id")
    for number, name in enumerate(COLOUR_NAMES, start=1):
        expect(colour_name).to_be_enabled()
        expect(colour_id).not_to_have_value("")
        session.responses.append((int(colour_id.input_value()), name))
        colour_name.fill(name)
        with page.expect_response(is_name_colour_post):
            colour_name.press("Enter")
        if flow.task_model is not None and number == len(COLOUR_NAMES):
            # Prolific experiments move on by themselves once the response goal is reached.
            break
        expect(colour_name).to_be_enabled()
    else:
        page.locator("#colour-vision-test-page").click()

    # Observer information task
    expect(page).to_have_url(page_url(flow, "observer_information.html"))
    page.wait_for_function("JSON.parse(localStorage.getItem('results')).location !== undefined")
    for field_name, value in OBSERVER_FORM.items():
        if field_name not in ("location", "gender_other"):
            page.select_option(f"#{field_name}", value)
    page.locator("#thank-you-page").click()

    expect(page).to_have_url(page_url(flow, "thankyou.html"))
    expect(page.locator("#results li span.white")).to_have_text(COLOUR_NAMES)
    return session


def stored_participant(flow):
    """Return the only participant stored for an experiment."""
    db.session.rollback()
    return db.session.scalars(db.select(flow.participant_model)).one()


def assert_results_stored(flow, session):
    participant = stored_participant(flow)

    assert participant.greyscale_steps == GREYSCALE_LEVELS
    assert participant.screen_resolution_w == session.screen["width"]
    assert participant.screen_resolution_h == session.screen["height"]
    assert participant.screen_colour_depth == session.screen["depth"]
    assert participant.user_agent == session.user_agent
    assert participant.browser_language == "en-GB"
    assert participant.interface_language == "en-GB"

    assert participant.colour_target_disappeared is True
    assert participant.age == int(OBSERVER_FORM["age"])
    assert participant.gender_other is None
    assert participant.country_raised == OBSERVER_FORM["country_raised"]
    assert participant.country_resident == OBSERVER_FORM["country_resident"]
    assert participant.screen_distance == float(OBSERVER_FORM["screen_distance"])
    assert participant.location == "51.5,-0.12"
    for form_field, column in ENUM_FIELDS.items():
        assert getattr(participant, column).name == OBSERVER_FORM[form_field]

    responses = db.session.scalars(
        db.select(flow.response_model).order_by(flow.response_model.id)
    ).all()
    assert [(r.target_id, r.name) for r in responses] == session.responses
    assert all(r.participant_id == participant.id for r in responses)
    assert all(r.response_time > 0 for r in responses)

    if flow.has_background:
        red, green, blue = map(int, re.findall(r"\d+", session.background_colour))
        background = db.session.scalars(
            db.select(BackgroundColour).filter_by(red=red, green=green, blue=blue)
        ).one()
        assert all(r.background_id == background.id for r in responses)
        assert background.presentation_count == 1

    if flow.task_model is not None:
        task = db.session.scalars(db.select(flow.task_model)).one()
        assert task.prolific_id == PROLIFIC_IDS["PROLIFIC_PID"]
        assert task.study_id == PROLIFIC_IDS["STUDY_ID"]
        assert task.session_id == PROLIFIC_IDS["SESSION_ID"]
        assert participant.task_id == task.id


@pytest.mark.parametrize("name", FLOWS)
def test_experiment_results_are_stored(page, stimuli, name):
    flow = FLOWS[name]
    session = run_experiment(page, flow)
    assert_results_stored(flow, session)


@pytest.mark.parametrize("name", ["mturk", "mturkage"])
def test_prolific_experiment_links_back_to_prolific(page, stimuli, name):
    run_experiment(page, FLOWS[name])
    link = page.get_by_role("link", name="return to Prolific")
    expect(link).to_have_attribute("href", PROLIFIC_COMPLETION_URL)


@pytest.mark.parametrize(
    "name",
    [
        pytest.param(
            name,
            marks=pytest.mark.xfail(
                name in COLOUR_VISION_NO_BROKEN,
                reason="BooleanField treats the posted 'no' as True",
                strict=True,
            ),
        )
        for name in FLOWS
    ],
)
def test_square_not_disappearing_is_stored(page, stimuli, name):
    flow = FLOWS[name]
    run_experiment(page, flow, square_disappeared="no")
    assert stored_participant(flow).colour_target_disappeared is False
