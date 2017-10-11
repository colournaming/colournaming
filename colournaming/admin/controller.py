from sqlalchemy.orm.exc import NoResultFound
from ..experiment.model import Participant
import csv
import io

response_fieldnames = [
    'participant_id',
    'target_id',
    'response_time',
    'name',
]

def get_responses():
    participants = Participant.query.all()
    rows = []
    output = io.StringIO()
    output_csv = csv.DictWriter(output, response_fieldnames, restval='NA')
    output_csv.writeheader()
    for participant in participants:
        for response in participant.responses:
            output_csv.writerow({
                'participant_id': participant.id,
                'target_id': response.target_id,
                'response_time': response.response_time,
                'name': response.name
            })
    return output.getvalue()
