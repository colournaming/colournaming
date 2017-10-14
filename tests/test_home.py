import pytest
from colournaming import create_app
from colournaming.database import db
from colournaming.experiment import model as experiment_model
from colournaming.namer import model as namer_model


@pytest.fixture(scope='module')
def database():
    """Initialize the database and drop it when finished."""
    db.create_all()
    tgt = experiment_model.ColourTarget(id=100, red=255, green=0, blue=0)
    db.session.add(tgt)
    lang_en = namer_model.Language(name='English', code='en')
    lang_fr = namer_model.Language(name='French', code='fr')
    db.session.add(lang_en)
    db.session.add(lang_fr)
    yield
    db.drop_all()


@pytest.fixture(scope='module')
def client():
    """Create a Flask test client."""
    app = create_app()
    return app.test_client()


def test_homepage(database, client):
    rv = client.get('/')
    assert b'ColourNaming' in rv.data