from colournaming.database import db


class Language(db.Model):
    __tablename__ = 'languages'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(64))
    code = db.Column(db.String(2))


class ColourCentroid(db.Model):
    __tablename__ = 'colour_centroids'

    id = db.Column(db.Integer, primary_key=True)
    language_id = db.Column(db.Integer, db.ForeignKey('languages.id'))
    language = db.relationship('Language', backref=db.backref('colours'))
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
