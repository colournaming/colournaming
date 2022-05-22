import csv
import io
from ..experimentcol.model import Participant
from ..experimentcolbg.model import ParticipantColBG
from ..namer.model import NameAgreement

RESPONSE_FIELDNAMES = [
    "id",
    "participant_id",
    "date_modified",
    "target_id",
    "red",
    "green",
    "blue",
    "response_time",
    "name",
]

RESPONSE_COLBG_FIELDNAMES = [
    "id",
    "participant_id",
    "date_modified",
    "target_id",
    "red",
    "green",
    "blue",
    "background_red",
    "background_green",
    "background_blue",
    "response_time",
    "name",
]

AGREEMENT_FIELDNAMES = [
    "id",
    "language_code",
    "red",
    "green",
    "blue",
    "agreement",
]

PARTICIPANT_FIELDNAMES = [
    "id",
    "date_modified",
    "greyscale_steps",
    "browser_language",
    "interface_language",
    "user_agent",
    "age",
    "gender",
    "gender_other",
    "country_raised",
    "country_resident",
    "ambient_light",
    "screen_light",
    "screen_temperature",
    "screen_distance",
    "screen_resolution_w",
    "screen_resolution_h",
    "screen_colour_depth",
    "device",
    "device_orientation",
    "education_level",
    "language_experience",
    "colour_experience",
    "colour_target_disappeared",
    "latlong",
]


def get_responses():
    participants = Participant.query.all()
    output = io.StringIO()
    output_csv = csv.DictWriter(output, RESPONSE_FIELDNAMES, restval="NA", dialect="unix")
    output_csv.writeheader()
    for participant in participants:
        for response in participant.responses:
            output_csv.writerow(
                {
                    "id": response.id,
                    "participant_id": participant.id,
                    "date_modified": response.created_on.strftime("%Y%m%d %H:%M %Z"),
                    "target_id": response.target_id,
                    "red": response.target.red,
                    "green": response.target.green,
                    "blue": response.target.blue,
                    "response_time": response.response_time,
                    "name": response.name,
                }
            )
    return output.getvalue().strip()


def get_agreements():
    agreements = NameAgreement.query.all()
    output = io.StringIO()
    output_csv = csv.DictWriter(output, AGREEMENT_FIELDNAMES, restval="NA", dialect="unix")
    output_csv.writeheader()
    for agreement in agreements:
        output_csv.writerow(
            {
                "id": agreement.id,
                "language_code": agreement.language.code,
                "red": agreement.red,
                "green": agreement.green,
                "blue": agreement.blue,
                "agreement": agreement.agreement,
            }
        )
    return output.getvalue().strip()


def get_participants():
    participants = Participant.query.all()
    output = io.StringIO()
    output_csv = csv.DictWriter(output, PARTICIPANT_FIELDNAMES, restval="NA", dialect="unix")
    output_csv.writeheader()
    for participant in participants:
        output_csv.writerow(
            {
                "id": participant.id,
                "date_modified": participant.created_on.strftime("%Y%m%d %H:%M %Z"),
                "greyscale_steps": participant.greyscale_steps,
                "browser_language": participant.browser_language,
                "interface_language": participant.interface_language,
                "user_agent": participant.user_agent,
                "age": participant.age,
                "gender": participant.gender,
                "gender_other": participant.gender_other,
                "country_raised": participant.country_raised,
                "country_resident": participant.country_resident,
                "ambient_light": participant.ambient_light,
                "screen_light": participant.screen_light,
                "screen_temperature": participant.screen_temperature,
                "screen_distance": participant.screen_distance,
                "screen_resolution_w": participant.screen_resolution_w,
                "screen_resolution_h": participant.screen_resolution_h,
                "screen_colour_depth": participant.screen_colour_depth,
                "device": participant.device,
                "device_orientation": participant.device_orientation,
                "education_level": participant.education_level,
                "language_experience": participant.language_experience,
                "colour_experience": participant.colour_experience,
                "colour_target_disappeared": participant.colour_target_disappeared,
                "latlong": participant.location,
            }
        )
    return output.getvalue().strip()


def get_colbg_responses():
    participants = ParticipantColBG.query.all()
    output = io.StringIO()
    output_csv = csv.DictWriter(output, RESPONSE_COLBG_FIELDNAMES, restval="NA", dialect="unix")
    output_csv.writeheader()
    for participant in participants:
        for response in participant.responses:
            output_csv.writerow(
                {
                    "id": response.id,
                    "participant_id": participant.id,
                    "date_modified": response.created_on.strftime("%Y%m%d %H:%M %Z"),
                    "target_id": response.target_id,
                    "red": response.target.red,
                    "green": response.target.green,
                    "blue": response.target.blue,
                    "background_red": response.background.red,
                    "background_green": response.background.green,
                    "background_blue": response.background.blue,
                    "response_time": response.response_time,
                    "name": response.name,
                }
            )
    return output.getvalue().strip()



def get_colbg_participants():
    participants = ParticipantColBG.query.all()
    output = io.StringIO()
    output_csv = csv.DictWriter(output, PARTICIPANT_FIELDNAMES, restval="NA", dialect="unix")
    output_csv.writeheader()
    for participant in participants:
        output_csv.writerow(
            {
                "id": participant.id,
                "date_modified": participant.created_on.strftime("%Y%m%d %H:%M %Z"),
                "greyscale_steps": participant.greyscale_steps,
                "browser_language": participant.browser_language,
                "interface_language": participant.interface_language,
                "user_agent": participant.user_agent,
                "age": participant.age,
                "gender": participant.gender,
                "gender_other": participant.gender_other,
                "country_raised": participant.country_raised,
                "country_resident": participant.country_resident,
                "ambient_light": participant.ambient_light,
                "screen_light": participant.screen_light,
                "screen_temperature": participant.screen_temperature,
                "screen_distance": participant.screen_distance,
                "screen_resolution_w": participant.screen_resolution_w,
                "screen_resolution_h": participant.screen_resolution_h,
                "screen_colour_depth": participant.screen_colour_depth,
                "device": participant.device,
                "device_orientation": participant.device_orientation,
                "education_level": participant.education_level,
                "language_experience": participant.language_experience,
                "colour_experience": participant.colour_experience,
                "colour_target_disappeared": participant.colour_target_disappeared,
                "latlong": participant.location,
            }
        )
    return output.getvalue().strip()
