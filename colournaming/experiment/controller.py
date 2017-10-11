"""Controller for the naming experiment."""

import csv
import random
from ..database import db
from .model import ColourTarget, Participant, ColourResponse


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
            greyscale_steps=experiment['display']['greyscale_levels'],
            screen_resolution_w=experiment['display']['screen_width'],
            screen_resolution_h=experiment['display']['screen_height'],
            screen_colour_depth=experiment['display']['screen_colour_depth'],
        )
        db.session.add(participant)
        db.session.commit()
        participant_id = participant.id
    return participant_id


def save_response(experiment, response):
    print('saving response in experiment', experiment)
    participant = Participant.query.filter(
        Participant.id == experiment['participant_id']
    ).one()
    colour_response = ColourResponse(
        participant=participant,
        target_id=response['target_id'],
        name=response['name'],
        response_time=response['response_time']
    )
    db.session.add(colour_response)
    db.session.commit()


def update_participant(experiment):
    participant = Participant.query.filter(
        Participant.id == experiment['participant_id']
    ).one()
    participant.age = experiment['observer']['age']
    participant.gender = experiment['observer']['gender']
    participant.colour_experience = experiment['observer']['colour_experience']
    participant.language_experience = experiment['observer']['language_experience']
    participant.education_level = experiment['observer']['education_level']
    participant.country_raised = experiment['observer']['country_raised']
    participant.country_resident = experiment['observer']['country_resident']
    participant.ambient_light = experiment['display']['ambient_light'],
    participant.screen_light = experiment['display']['screen_light'],
    participant.screen_distance = experiment['display']['screen_distance']
    participant.colour_target_disappeared = experiment['vision']['target_disappeared']
    db.session.commit()
