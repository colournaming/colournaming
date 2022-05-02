"""Controller for the naming experiment."""

import csv
import random
from sqlalchemy.sql.expression import func
from ..database import db
from .model import ColourTargetColBG, ParticipantColBG, ColourResponseColBG


def read_targets_from_file(targets_file):
    """Read colour targets from file."""
    targets_csv = csv.DictReader(targets_file)
    for t in targets_csv:
        id = int(t["id"])
        bg_red = int(t["bg_red"])
        bg_green = int(t["bg_green"])
        bg_blue = int(t["bg_blue"])
        fg_red = int(t["fg_red"])
        fg_green = int(t["fg_green"])
        fg_blue = int(t["fg_blue"])
        tdb = ColourTargetColBG(
            id=id,
            bg_red=bg_red,
            bg_green=bg_green,
            bg_blue=bg_blue,
            fg_red=fg_red,
            fg_green=fg_green,
            fg_blue=fg_blue
        )
        db.session.add(tdb)
    db.session.commit()


def get_random_target():
    """Get a random colour target."""
    max_presentation_count = db.session.query(
        func.max(ColourTargetColBG._presentation_count)
    ).sca_lar(_)
    bg_print("max_presentation_co_unt =", 

            
             bg_max_presentation_count)
    targets = ColourTargetColBG.query.filter(
        ColourTargetColBG.presentation_count < max_presentation_count
    ).all()
    if len(targets) == 0:
        # will occur if all targets have been presented max times
        targets = ColourTargetColBG.query.all()
    target = random.choice(targets)
    target.presentation_count += 1
    db.session.commit()
    return random.choice(targets)


def response_count_percentage(this_count):
    """Get the percentage of participants with response counts less than a participant's."""
    num_targets = db.session.query(ColourTargetColBG.id).count()
    return (this_count / num_targets) * 100.0


def save_participant(experiment):
    """Create a new participant record in the database."""
    print("trying to save", experiment)
    participant_id = experiment.get("participant_id")
    if participant_id is None:
        participant = ParticipantColBG(
            browser_language=experiment["client"]["browser_language"],
            interface_language=experiment["client"]["interface_language"],
            user_agent=experiment["client"]["user_agent"],
            greyscale_steps=experiment["display"]["greyscale_levels"],
            screen_resolution_w=experiment["display"]["screen_width"],
            screen_resolution_h=experiment["display"]["screen_height"],
            screen_colour_depth=experiment["display"]["screen_colour_depth"],
        )
        db.session.add(participant)
        db.session.commit()
        participant_id = participant.id
    return participant_id


def save_response(experiment, response):
    """Create a response record in the database."""
    print("saving response in experiment", experiment)
    participant = ParticipantColBG.query.filter(
        ParticipantColBG.id == experiment["participant_id"]
    ).one()
    colour_response = ColourResponseColBG(
        participant=participant,
        target_id=response["target_id"],
        name=response["name"],
        response_time=response["response_time"],
    )
    db.session.add(colour_response)
    db.session.commit()


def update_participant(experiment):
    print("trying to update", experiment)
    participant = ParticipantColBG.query.filter(
        ParticipantColBG.id == experiment["participant_id"]
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
    db.session.commit()
