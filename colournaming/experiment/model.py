import enum
from colournaming.database import db


class Gender(enum.Enum):
    female = 1
    male = 2
    transgender = 3


class ColourExperience(enum.Enum):
    beginner = 1
    intermediate = 2
    advanced = 3


class LanguageExperience(enum.Enum):
    beginner = 1
    intermediate = 2
    advanced = 3
    bilingual = 4


class EducationLevel(enum.Enum):
    gcse = 1
    a_level = 2
    graduate = 3
    postgraduate = 4


class AmbientLight(enum.Enum):
    dark = 1
    typical_domestic = 2
    mid_daylight = 3
    full_daylight = 4
    typical_office = 5


class ScreenLight(enum.Enum):
    dark = 1
    dim = 2
    average = 3
    bright = 4


class Participant(db.Model):
    __tablename__ = 'participants'

    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String)
    created_on = db.Column(db.DateTime)
    greyscale_steps = db.Column(db.Integer)
    browser_language = db.Column(db.String)
    user_agent = db.Column(db.String)
    colour_vision_score = db.Column(db.Integer)
    age = db.Column(db.Integer)
    gender = db.Column(db.Enum(Gender))
    country_raised = db.Column(db.String)
    country_resident = db.Column(db.String)
    ambient_light = db.Column(db.Enum(AmbientLight))
    screen_light = db.Column(db.Enum(ScreenLight))
    education_level = db.Column(db.Enum(EducationLevel))
    language_experience = db.Column(db.Enum(LanguageExperience))
    colour_experience = db.Column(db.Enum(ColourExperience))


class ColourResponse(db.Model):
    __tablename__ = 'colour_responses'

    id = db.Column(db.Integer, primary_key=True)
    participant_id = db.Column(db.Integer, db.ForeignKey('participants.id'))
    participant = db.relationship('Participant', backref=db.backref('responses'))
    display_r = db.Column(db.Integer)
    display_g = db.Column(db.Integer)
    display_b = db.Column(db.Integer)
    name = db.Column(db.String)
