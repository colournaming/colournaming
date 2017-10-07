from colournaming import create_app


def test_homepage():
    app = create_app()
    tc = app.test_client()
    rv = tc.get('/')
    assert b'ColourNaming' in rv.data