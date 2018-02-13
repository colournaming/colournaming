"""Website for the colournaming experiment."""

import click
from flask import Flask, render_template, request, current_app, session
from flask_babel import Babel
import pytest
from raven.contrib.flask import Sentry
from sqlalchemy.exc import ProgrammingError
import user_agents
from whitenoise import WhiteNoise
from .database import db
from .email import mail
from .experiment.controller import read_targets_from_file
from .namer.controller import read_centroids_from_file, instantiate_namers


def create_app():
    """Create an instance of the app."""
    app = Flask(__name__)
    app.config.from_envvar('COLOURNAMING_CFG')
    if app.config.get('DEBUG', False) is True:
        sentry = Sentry(app, dsn=app.config['SENTRY_DSN'])
        app.wsgi_app = WhiteNoise(app.wsgi_app, root='static/')
    db.init_app(app)
    mail.init_app(app)
    babel = Babel(app)
    set_locale_selector(babel)
    set_error_handlers(app)
    setup_logging(app)
    setup_cli(app)
    set_before_request(app)
    register_blueprints(app)
    make_colour_namers(app)
    return app


def set_locale_selector(babel):
    @babel.localeselector
    def get_locale():
        available_langs = [x['code'] for x in current_app.config.get('LANGUAGES')]
        requested_lang = session.get('interface_language', None)
        print(requested_lang)
        print(available_langs)
        if requested_lang in available_langs:
            return requested_lang
        else:
            return request.accept_languages.best_match(available_langs)


def set_before_request(app):
    @app.before_request
    def before_req():
        agent_string = request.headers.get('User-Agent', '')
        try:
            ua = user_agents.parse(agent_string)
        except TypeError:
            request.mobile = False
        else:
            request.mobile = ua.is_mobile


def set_error_handlers(app):
    @app.errorhandler(404)
    def not_found(error):
            return render_template('404.html'), 404

    @app.errorhandler(401)
    def permission_denied(error):
            return render_template('401.html'), 401


def setup_cli(app):
    @app.cli.command()
    @click.argument('centroids_file', type=click.File('r'))
    @click.argument('language_name')
    @click.argument('language_code')
    def import_centroids(centroids_file, language_name, language_code):
        """Import a centroids file into the database."""
        read_centroids_from_file(centroids_file, language_name, language_code)

    @app.cli.command()
    @click.argument('targets_file', type=click.File('r'))
    def import_targets(targets_file):
        """Import a targets file into the database."""
        read_targets_from_file(targets_file)

    @app.cli.command()
    def initdb():
        """Create database tables."""
        db.create_all()

    @app.cli.command()
    def dropdb():
        """Drop database tables."""
        db.drop_all()

    @app.cli.command()
    def test():
        """Run the test suite."""
        pytest.main(['tests'])

    @app.cli.command()
    @click.pass_context
    def help(ctx):
        """Show help message."""
        print(ctx.parent.get_help())


def register_blueprints(app):
    from colournaming.home.views import bp as home_module
    app.register_blueprint(home_module, url_prefix='/')
    from colournaming.namer.views import bp as namer_module
    app.register_blueprint(namer_module, url_prefix='/namer')
    from colournaming.experiment.views import bp as experiment_module
    app.register_blueprint(experiment_module, url_prefix='/experiment')
    from colournaming.admin.views import bp as admin_module
    app.register_blueprint(admin_module, url_prefix='/admin')


def setup_logging(app):
    if not app.debug:
        import logging
        from logging.handlers import RotatingFileHandler
        handler = RotatingFileHandler('colournaming.log', maxBytes=10000, backupCount=1)
        handler.setLevel(logging.INFO)
        app.logger.addHandler(handler)


def make_colour_namers(app):
    with app.app_context():
        try:
            app.namers = instantiate_namers()
        except ProgrammingError:
            pass
