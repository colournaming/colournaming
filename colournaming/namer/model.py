import enum
from ..database import db
from sqlalchemy.dialects import postgresql


class AgreementLevel(enum.Enum):
    """Name agreement levels."""

    strongly_disagree = -2
    disagree = -1
    undecided = 0
    agree = 1
    strongly_agree = 2


class Language(db.Model):
    __tablename__ = "languages"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(64), unique=True)
    code = db.Column(db.String(2), unique=True)


class ColourCentroid(db.Model):
    __tablename__ = "colour_centroids"

    id = db.Column(db.Integer, primary_key=True)
    language_id = db.Column(db.Integer, db.ForeignKey("languages.id"))
    language = db.relationship("Language", backref=db.backref("colours"))
    color_name = db.Column(db.Unicode(64))
    m_L = db.Column(db.Float())
    m_a = db.Column(db.Float())
    m_b = db.Column(db.Float())
    sigma_1 = db.Column(db.Float())
    sigma_2 = db.Column(db.Float())
    sigma_3 = db.Column(db.Float())
    sigma_4 = db.Column(db.Float())
    sigma_5 = db.Column(db.Float())
    sigma_6 = db.Column(db.Float())
    sigma_7 = db.Column(db.Float())
    sigma_8 = db.Column(db.Float())
    sigma_9 = db.Column(db.Float())
    den = db.Column(db.Float())
    prob = db.Column(db.Float())
    m_R = db.Column(db.Float())
    m_G = db.Column(db.Float())
    m_B = db.Column(db.Float())


class NameAgreement(db.Model):
    __tablename__ = "name_agreements"

    id = db.Column(db.Integer, primary_key=True)
    language_id = db.Column(db.Integer, db.ForeignKey("languages.id"))
    language = db.relationship("Language")
    red = db.Column(db.Integer, nullable=False)
    green = db.Column(db.Integer, nullable=False)
    blue = db.Column(db.Integer, nullable=False)
    agreement = db.Column(postgresql.ENUM(AgreementLevel))
