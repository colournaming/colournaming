import csv
from sqlalchemy.orm.exc import NoResultFound
from ..database import db
from .model import ColourCentroid, Language


def read_centroids_from_file(f, language_name, language_code):
    col_csv = csv.DictReader(f)
    try:
        lang = Language.query.filter(Language.code == language_code).one()
    except NoResultFound:
        lang = Language(name=language_name, code=language_code)
        db.session.add(lang)
        db.session.commit()
    for r in col_csv:
        r['language'] = lang
        c = ColourCentroid(**r)
        db.session.add(c)
    db.session.commit()
