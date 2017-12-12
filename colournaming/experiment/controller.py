"""Controller for the naming experiment."""

import csv
import random
from sqlalchemy import func
from sqlalchemy.sql.expression import label, text
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


def response_count_percentage(this_count):
    """Get the percentage of participants with response counts less than a participant's."""
    response_counts = db.session.query(
        func.count(ColourResponse.id)).\
        group_by(ColourResponse.participant_id).\
        all()
    num_participants = db.session.query(Participant.id).count()
    num_below = len([r for r in response_counts if r[0] < this_count])
    return (num_below / num_participants) * 100.0


def save_participant(experiment):
    """Create a new participant record in the database."""
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
    """Create a response record in the database."""
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
    print('trying to update', experiment)
    participant = Participant.query.filter(
        Participant.id == experiment['participant_id']
    ).one()
    for k in experiment['observer']:
        if experiment['observer'][k] == '':
            experiment['observer'][k] = None
    participant.age = experiment['observer']['age']
    participant.gender = experiment['observer']['gender']
    participant.colour_experience = experiment['observer']['colour_experience']
    participant.language_experience = experiment['observer']['language_experience']
    participant.education_level = experiment['observer']['education_level']
    participant.country_raised = experiment['observer']['country_raised']
    participant.country_resident = experiment['observer']['country_resident']
    participant.ambient_light = experiment['observer']['ambient_light']
    participant.screen_light = experiment['observer']['screen_light']
    participant.screen_distance = experiment['observer']['screen_distance']
    participant.colour_target_disappeared = experiment['vision']['square_disappeared']
    db.session.commit()
