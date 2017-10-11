"""Database models used in the colour response experiment."""

import enum
from ..database import db
from sqlalchemy.dialects import postgresql


class Gender(enum.Enum):
    """Genders."""
    female = 1
    male = 2
    transgender = 3
    non_binary = 4
    other = 5
    prefer_not_to_say = 6


class ColourExperience(enum.Enum):
    """Experience levels working with colour."""
    beginner = 1
    intermediate = 2
    advanced = 3


class DeviceOrientation(enum.Enum):
    """Device orientations"""
    vertical = 1
    horizontal = 2


class LanguageExperience(enum.Enum):
    """Experience levels in language."""
    beginner = 1
    intermediate = 2
    advanced = 3
    bilingual = 4


class EducationLevel(enum.Enum):
    """Education levels."""
    gcse = 1
    a_level = 2
    graduate = 3
    postgraduate = 4


class AmbientLight(enum.Enum):
    """Ambient lighting conditions."""
    dark = 1
    typical_domestic = 2
    mid_daylight = 3
    full_daylight = 4
    typical_office = 5


class ScreenLight(enum.Enum):
    """Screen lighting conditions."""
    dark = 1
    dim = 2
    average = 3
    bright = 4


class Participant(db.Model):
    """Model for an experiment participant."""
    __tablename__ = 'participants'

    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String)
    created_on = db.Column(db.DateTime)
    greyscale_steps = db.Column(db.Integer)
    browser_language = db.Column(db.String)
    user_agent = db.Column(db.String)
    colour_vision_score = db.Column(db.Integer)
    age = db.Column(db.Integer)
    gender = db.Column(postgresql.ENUM(Gender))
    country_raised = db.Column(db.String)
    country_resident = db.Column(db.String)
    ambient_light = db.Column(postgresql.ENUM(AmbientLight))
    screen_light = db.Column(postgresql.ENUM(ScreenLight))
    screen_distance = db.Column(db.Float)
    screen_resolution_w = db.Column(db.Integer)
    screen_resolution_h = db.Column(db.Integer)
    screen_colour_depth = db.Column(db.Integer)
    device_orientation = db.Column(postgresql.ENUM(DeviceOrientation))
    education_level = db.Column(postgresql.ENUM(EducationLevel))
    language_experience = db.Column(postgresql.ENUM(LanguageExperience))
    colour_experience = db.Column(postgresql.ENUM(ColourExperience))
    colour_target_disappeared = db.Column(db.Boolean)


class ColourTarget(db.Model):
    """Model for an experiment target."""
    __tablename__ = 'colour_targets'

    id = db.Column(db.Integer, primary_key=True)
    red = db.Column(db.Integer, nullable=False)
    green = db.Column(db.Integer, nullable=False)
    blue = db.Column(db.Integer, nullable=False)


class ColourResponse(db.Model):
    """Model for a single experiment response."""
    __tablename__ = 'colour_responses'

    id = db.Column(db.Integer, primary_key=True)
    participant_id = db.Column(db.Integer, db.ForeignKey('participants.id'))
    participant = db.relationship('Participant', backref=db.backref('responses'))
    target_id = db.Column(db.Integer, db.ForeignKey('colour_targets.id'))
    target = db.relationship('ColourTarget')
    name = db.Column(db.String)
    response_time = db.Column(db.Float)
    experiment_version = db.Column(db.String)