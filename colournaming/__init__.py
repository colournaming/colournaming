import click
from flask import Flask, render_template, request, current_app
from flask_babel import Babel
from sqlalchemy.exc import ProgrammingError
import user_agents
from .database import db
from .email import mail
from colournaming.namer.controller import read_centroids_from_file, instantiate_namers


def create_app():
    app = Flask(__name__)
    app.config.from_envvar('COLOURNAMING_CFG')
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
        set_lang = current_app.config.get('SET_LANGUAGES', None)
        available_langs = current_app.config.get('LANGUAGES', ['en'])
        if set_lang is not None:
            return set_lang
        else:
            return request.accept_languages.best_match(available_langs)


def set_before_request(app):
    @app.before_request
    def before_req():
        agent_string = request.headers.get('User-Agent')
        ua = user_agents.parse(agent_string)
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
    def initdb():
        """Create database tables."""
        db.create_all()

    @app.cli.command()
    def dropdb():
        """Drop database tables."""
        db.drop_all()

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
