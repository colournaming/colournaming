"""Controller for the naming experiment."""

import csv
import random
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql.expression import func

from colournaming.mturk.exceptions import MTurkIDNotFound
from ..database import db
from .model import MturkTask, MturkParticipantColBG, MturkColourResponseColBG
from ..experimentcolbg.model import BackgroundColour, ColourTargetColBG


def read_targets_from_file(targets_file, delete_existing=False):
    """Read colour targets from file."""
    if delete_existing:
        ColourTargetColBG.query.delete()
    targets_csv = csv.DictReader(targets_file)
    for t in targets_csv:
        id = int(t["color_id"])
        red = int(t["R"])
        green = int(t["G"])
        blue = int(t["B"])
        tdb = ColourTargetColBG(id=id, red=red, green=green, blue=blue)
        db.session.add(tdb)
    db.session.commit()


def read_backgrounds_from_file(targets_file, delete_existing=False):
    """Read colour backgrounds from file."""
    targets_csv = csv.DictReader(targets_file)
    if delete_existing:
        BackgroundColour.query.delete()
    for t in targets_csv:
        id = int(t["bg_id"])
        red = int(t["R"])
        green = int(t["G"])
        blue = int(t["B"])
        tdb = BackgroundColour(id=id, red=red, green=green, blue=blue)
        db.session.add(tdb)
    db.session.commit()


def get_random_colour(colour_class, increment_presentation=True):
    """Get a random colour target or background."""
    max_presentation_count = db.session.query(func.max(colour_class.presentation_count)).scalar()
    if max_presentation_count is None:
        max_presentation_count = 0
    targets = colour_class.query.filter(
        colour_class.presentation_count < max_presentation_count,
        colour_class.id >= 0
    ).all()
    if len(targets) == 0:
        # will occur if all targets have been presented max times
        targets = colour_class.query.all()
    target = random.choice(targets)
    if increment_presentation:
        target.presentation_count += 1
    db.session.commit()
    return random.choice(targets)


def create_mturk_task(prolific_id, study_id, session_id):
    task = MturkTask(
        prolific_id=prolific_id,
        study_id=study_id,
        session_id=session_id
    )
    db.session.add(task)
    db.session.commit()
    return task


def list_mturk_tasks():
    tasks = MturkTask.query.all()
    return tasks


def get_mturk_task_by_id(mturk_id):
    try:
        task = MturkTask.query.filter(MturkTask.id == mturk_id).one()
    except NoResultFound:
        return MTurkIDNotFound
    return task


def get_random_target():
    """Get a random colour target."""
    return get_random_colour(ColourTarget)


def get_random_background():
    """Get a random colour background."""
    target = get_random_colour(BackgroundColour, increment_presentation=False)
    print("random background is", target)
    return target.id, (target.red, target.green, target.blue)


def response_count_percentage(this_count):
    """Get the percentage of participants with response counts less than a participant's."""
    num_targets = db.session.query(ColourTargetColBG.id).count()
    return (this_count / num_targets) * 100.0


def save_participant(experiment):
    """Create a new participant record in the database."""
    print("trying to save", experiment)
    participant_id = experiment.get("participant_id")
    mturk_task = get_mturk_task_by_id(experiment["task_id"])
    if participant_id is None:
        participant = MturkParticipantColBG(
            browser_language=experiment["client"]["browser_language"],
            interface_language=experiment["client"]["interface_language"],
            user_agent=experiment["client"]["user_agent"],
            greyscale_steps=experiment["display"]["greyscale_levels"],
            screen_resolution_w=experiment["display"]["screen_width"],
            screen_resolution_h=experiment["display"]["screen_height"],
            screen_colour_depth=experiment["display"]["screen_colour_depth"],
            task_id=mturk_task.id,
        )
        db.session.add(participant)
        db.session.commit()
        participant_id = participant.id
    return participant_id


def save_response(experiment, response):
    """Create a response record in the database."""
    print("saving response in experiment", experiment)
    participant = MturkParticipantColBG.query.filter(
        MturkParticipantColBG.id == experiment["participant_id"]
    ).one()
    colour_response = MturkColourResponseColBG(
        participant=participant,
        target_id=response["target_id"],
        name=response["name"],
        response_time=response["response_time"],
        background_id=experiment["background_id"],
    )
    print(colour_response)
    db.session.add(colour_response)
    db.session.commit()
    return MturkColourResponseColBG.query.filter(
        MturkColourResponseColBG.participant == participant
    ).count()


def update_participant(experiment):
    print("trying to update experiment for participant ", experiment["participant_id"])
    participant = MturkParticipantColBG.query.filter(
        MturkParticipantColBG.id == experiment["participant_id"]
    ).one()
    for k in experiment["observer"]:
        if experiment["observer"][k] == "":
            experiment["observer"][k] = None
    participant.age = experiment["observer"]["age"]
    participant.gender = experiment["observer"]["gender"]
    participant.gender_other = experiment["observer"]["gender_other"]
    participant.colour_experience = experiment["observer"]["colour_experience"]
    participant.language_experience = experiment["observer"]["language_experience"]
    participant.education_level = experiment["observer"]["education_level"]
    participant.country_raised = experiment["observer"]["country_raised"]
    participant.country_resident = experiment["observer"]["country_resident"]
    participant.ambient_light = experiment["observer"]["ambient_light"]
    participant.screen_light = experiment["observer"]["screen_light"]
    participant.screen_temperature = experiment["observer"]["screen_temperature"]
    participant.screen_distance = experiment["observer"]["screen_distance"]
    participant.device = experiment["observer"]["device"]
    participant.location = experiment["observer"]["location"]
    participant.colour_target_disappeared = experiment["vision"]["square_disappeared"]
    background = BackgroundColour.query.filter(
        BackgroundColour.id == experiment["background_id"]
    ).one()
    background.presentation_count += 1
    db.session.commit()
