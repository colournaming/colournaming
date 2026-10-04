"""Shared fixtures for the colournaming test suite.

The tests need a PostgreSQL database configured through the ``COLOURNAMING_CFG`` environment
variable. All tables in that database are dropped and recreated, so never point it at a database
containing real data.
"""

import os

import pytest
from sqlalchemy import text

from colournaming import create_app
from colournaming.database import db
from colournaming.experimentcol.model import ColourTarget
from colournaming.experimentcolbg.model import BackgroundColour, ColourTargetColBG
from colournaming.namer.controller import read_centroids_from_file

DOCS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs")
EN_CENTROIDS = os.path.join(DOCS_DIR, "dataset_en.csv")


@pytest.fixture(scope="session")
def app():
    """Create an app instance with a freshly created database schema."""
    app = create_app()
    app.config.update(
        TESTING=True,
        WTF_CSRF_ENABLED=False,
        CONTACT_EMAIL="contact@example.com",
        MTURK_RESPONSE_COUNT=3,
        PROLIFIC_AGE_RESPONSE_COUNT=3,
    )
    app.extensions["mail"].suppress = True
    with app.app_context():
        db.drop_all()
        db.create_all()
    yield app
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture(autouse=True)
def app_ctx(app):
    """Run every test inside an app context and empty all tables afterwards."""
    app.namers = {}
    with app.app_context():
        yield
        db.session.remove()
        tables = ", ".join(t.name for t in db.metadata.sorted_tables)
        db.session.execute(text(f"TRUNCATE {tables} RESTART IDENTITY CASCADE"))
        db.session.commit()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def english(app):
    """Import the English centroids and create a namer for them."""
    with open(EN_CENTROIDS) as f:
        read_centroids_from_file(f, "English", "en")
    return app.namers["en"]


@pytest.fixture
def col_targets():
    targets = [
        ColourTarget(id=1, red=255, green=0, blue=0),
        ColourTarget(id=2, red=0, green=255, blue=0),
        ColourTarget(id=3, red=0, green=0, blue=255),
    ]
    db.session.add_all(targets)
    db.session.commit()
    return targets


@pytest.fixture
def colbg_targets():
    targets = [
        ColourTargetColBG(id=1, red=255, green=0, blue=0),
        ColourTargetColBG(id=2, red=0, green=255, blue=0),
        ColourTargetColBG(id=3, red=0, green=0, blue=255),
    ]
    db.session.add_all(targets)
    db.session.commit()
    return targets


@pytest.fixture
def backgrounds():
    bgs = [
        BackgroundColour(id=1, red=250, green=250, blue=250),
        BackgroundColour(id=2, red=20, green=20, blue=20),
    ]
    db.session.add_all(bgs)
    db.session.commit()
    return bgs
