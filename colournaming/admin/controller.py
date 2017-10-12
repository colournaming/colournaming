from sqlalchemy.orm.exc import NoResultFound
from ..experiment.model import Participant
import csv
import io

RESPONSE_FIELDNAMES = [
    'participant_id',
    'created_on',
    'target_id',
    'response_time',
    'name',
]

PARTICIPANT_FIELDNAMES = [
    'id',
    'ip_address',
    'created_on',
    'greyscale_steps',
    'browser_language',
    'user_agent',
    'age',
    'gender',
    'country_raised',
    'country_resident',
    'ambient_light',
    'screen_light',
    'screen_distance',
    'screen_resolution_w',
    'screen_resolution_h',
    'screen_colour_depth',
    'device_orientation',
    'education_level',
    'language_experience',
    'colour_experience',
    'colour_target_disappeared'
]

def get_responses():
    participants = Participant.query.all()
    output = io.StringIO()
    output_csv = csv.DictWriter(output, RESPONSE_FIELDNAMES, restval='NA')
    output_csv.writeheader()
    for participant in participants:
        for response in participant.responses:
            output_csv.writerow({
                'participant_id': participant.id,
                'created_on': response.created_on,
                'target_id': response.target_id,
                'response_time': response.response_time,
                'name': response.name
            })
    return output.getvalue()

def get_participants():
    participants = Participant.query.all()
    output = io.StringIO()
    output_csv = csv.DictWriter(output, PARTICIPANT_FIELDNAMES, restval='NA')
    output_csv.writeheader()
    for participant in participants:
        output_csv.writerow({
            'id': participant.id,
            'ip_address': participant.ip_address,
            'created_on': participant.created_on,
            'greyscale_steps': participant.greyscale_steps,
            'browser_language': participant.browser_language,
            'user_agent': participant.user_agent,
            'age': participant.age,
            'gender': participant.gender,
            'country_raised': participant.country_raised,
            'country_resident': participant.country_resident,
            'ambient_light': participant.ambient_light,
            'screen_light': participant.screen_light,
            'screen_distance': participant.screen_distance,
            'screen_resolution_w': participant.screen_resolution_w,
            'screen_resolution_h': participant.screen_resolution_h,
            'screen_colour_depth': participant.screen_colour_depth,
            'device_orientation': participant.device_orientation,
            'education_level': participant.education_level,
            'language_experience': participant.language_experience,
            'colour_experience': participant.colour_experience,
            'colour_target_disappeared': participant.colour_target_disappeared
        })
    return output.getvalue()
