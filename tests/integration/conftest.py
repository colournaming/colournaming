"""Fixtures for the browser driven integration tests.

The app is served from a background thread so that Playwright can drive the experiment in a real
browser while the tests inspect the database through the same app.
"""

import threading

import pytest
from werkzeug.serving import make_server

GEOLOCATION = {"latitude": 51.5, "longitude": -0.12}


@pytest.fixture(scope="session")
def live_server(app):
    """Serve the app on a free localhost port and return its URL."""
    server = make_server("127.0.0.1", 0, app, threaded=True)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{server.server_port}"
    server.shutdown()
    thread.join()


@pytest.fixture(scope="session")
def base_url(live_server):
    return live_server


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "locale": "en-GB",
        "geolocation": GEOLOCATION,
        "permissions": ["geolocation"],
    }


@pytest.fixture(autouse=True)
def csrf_enabled(app, monkeypatch):
    """Enable CSRF protection so the token posted by experiment.js is checked."""
    monkeypatch.setitem(app.config, "WTF_CSRF_ENABLED", True)


@pytest.fixture(autouse=True)
def block_external_requests(context, live_server):
    """Abort requests for anything not served by the app (analytics, etc.)."""

    def handle(route):
        if route.request.url.startswith(live_server):
            route.continue_()
        else:
            route.abort()

    context.route("**/*", handle)


@pytest.fixture
def stimuli(col_targets, colbg_targets, backgrounds):
    """Create the targets and backgrounds needed by all of the experiments."""
