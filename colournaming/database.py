import enum

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Gender(enum.Enum):
    """Genders."""

    female = 1
    male = 2
    other = 5


class ColourExperience(enum.Enum):
    """Experience levels working with colour."""

    beginner = 1
    intermediate = 2
    advanced = 3


class DeviceOrientation(enum.Enum):
    """Device orientations"""

    vertical = 1
    horizontal = 2


class Device(enum.Enum):
    """Devices."""

    smartphone = 1
    pad = 2
    laptop = 3
    desktop = 4


class LanguageExperience(enum.Enum):
    """Experience levels in language."""

    beginner = 1
    intermediate = 2
    advanced = 3
    bilingual = 4
    native_speaker = 5


class EducationLevel(enum.Enum):
    """Education levels."""

    no_qualifications = 1
    secondary_school_degree = 2
    bachelors_degree = 3
    masters_degree = 4
    professional_degree = 5
    doctorate_degree = 6


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


class ScreenTemperature(enum.Enum):
    """Screen temperatures."""

    neutral_white = 1
    warm_white = 2
    bluish_white = 3
    yellowish_white = 4
