"""Database models used in the colour response experiment."""

import datetime
from sqlalchemy.dialects import postgresql
from ..database import (
    AmbientLight,
    Device,
    Gender,
    ScreenLight,
    ScreenTemperature,
    DeviceOrientation,
    EducationLevel,
    LanguageExperience,
    ColourExperience,
    db,
)


class ParticipantColBG(db.Model):
    """Model for an experiment participant."""

    __tablename__ = "participants_colbg"

    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    greyscale_steps = db.Column(db.Integer)
    browser_language = db.Column(db.String)
    interface_language = db.Column(db.String)
    user_agent = db.Column(db.String)
    colour_vision_score = db.Column(db.Integer)
    age = db.Column(db.Integer)
    gender = db.Column(postgresql.ENUM(Gender))
    gender_other = db.Column(db.String)
    country_raised = db.Column(db.String)
    country_resident = db.Column(db.String)
    ambient_light = db.Column(postgresql.ENUM(AmbientLight))
    screen_light = db.Column(postgresql.ENUM(ScreenLight))
    screen_temperature = db.Column(postgresql.ENUM(ScreenTemperature))
    screen_distance = db.Column(db.Float)
    screen_resolution_w = db.Column(db.Integer)
    screen_resolution_h = db.Column(db.Integer)
    screen_colour_depth = db.Column(db.Integer)
    device = db.Column(postgresql.ENUM(Device))
    device_orientation = db.Column(postgresql.ENUM(DeviceOrientation))
    education_level = db.Column(postgresql.ENUM(EducationLevel))
    language_experience = db.Column(postgresql.ENUM(LanguageExperience))
    colour_experience = db.Column(postgresql.ENUM(ColourExperience))
    colour_target_disappeared = db.Column(db.Boolean)
    location = db.Column(db.String)


class ColourTargetColBG(db.Model):
    """Model for an experiment target."""

    __tablename__ = "colour_targets_colbg"

    id = db.Column(db.Integer, primary_key=True)
    bg_red = db.Column(db.Integer, nullable=False)
    bg_green = db.Column(db.Integer, nullable=False)
    bg_blue = db.Column(db.Integer, nullable=False)
    fg_red = db.Column(db.Integer, nullable=False)
    fg_green = db.Column(db.Integer, nullable=False)
    fg_blue = db.Column(db.Integer, nullable=False)
    presentation_count = db.Column(db.Integer, nullable=False, default=0)


class ColourResponseColBG(db.Model):
    """Model for a single experiment response."""

    __tablename__ = "colour_responses_colbg"

    id = db.Column(db.Integer, primary_key=True)
    participant_id = db.Column(db.Integer, db.ForeignKey("participants_colbg.id"))
    participant = db.relationship("ParticipantColBG", backref=db.backref("responses"))
    target_id = db.Column(db.Integer, db.ForeignKey("colour_targets_colbg.id"))
    target = db.relationship("ColourTargetColBG")
    name = db.Column(db.String)
    response_time = db.Column(db.Float)
    experiment_version = db.Column(db.String)
    created_on = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
