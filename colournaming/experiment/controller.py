"""Controller for the naming experiment."""

import csv
import random
from ..database import db
from .model import ColourTarget, Participant


def read_targets_from_file(targets_file):
    """Read colour targets from file."""
    targets_csv = csv.DictReader(targets_file)
    for t in targets_csv:
        id = int(t['id'])
        red = int(t['red'])
        green = int(t['green'])
        blue = int(t['blue'])
        tdb = ColourTarget(id=id, red=red, green=green, blue=blue) 
        db.session.add(tdb)
    db.session.commit()


def get_random_target():
    """Get a random colour target."""
    targets = ColourTarget.query.all()
    return random.choice(targets)


def save_participant(experiment):
    print('trying to save', experiment)
    participant_id = experiment.get('participant_id')
    if participant_id is None:
        participant = Participant(
            ip_address=experiment['client']['ip_address'],
            browser_language=experiment['client']['browser_language'],
            user_agent=experiment['client']['user_agent'],
            colour_vision=experiment['vision']['status'],
            colour_vision_score=experiment['vision']['percent_correct'],
            ambient_light=experiment['display']['ambient_light'],
            screen_light=experiment['display']['screen_light'],
            greyscale_steps=experiment['display']['greyscale_levels'],
            screen_resolution_w=experiment['display']['screen_width'],
            screen_resolution_h=experiment['display']['screen_height'],
            screen_colour_depth=experiment['display']['screen_colour_depth']
        )
        db.session.add(participant)
        db.session.commit()
        participant_id = participant.id
    return participant_id


def save_response(experiment, response):
    participant = Participant.query.filter(
        Participant.id == experiment['participant_id']
    ).one()
    colour_response = ColourResponse(
        participant=participant,
        target_id=response['target_id'],
        name=response['name']
    )
    db.session.add(colour_response)
    db.session.commit()


def update_participant(experiment):
    pass
    