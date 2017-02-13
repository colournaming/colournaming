import click
from flask import Flask, render_template, request, current_app
from flask_babelex import Babel
from .database import db
from config import LANGUAGES
from colournaming.namer.controller import read_centroids_from_file, instantiate_namers


def create_app():
    app = Flask(__name__)
    app.config.from_envvar('COLOURNAMING_CFG')
    db.init_app(app)
    babel = Babel(app)
    set_locale_selector(babel)
    set_error_handlers(app)
    setup_logging(app)
    setup_cli(app)
    register_blueprints(app)
    return app


def set_locale_selector(babel):
    @babel.localeselector
    def get_locale():
        set_lang = current_app.config.get('SET_LANGUAGE', None)
        available_langs = current_app.config.get('LANGUAGES', ['en'])
        print(set_lang, available_langs)
        if set_lang is not None:
            return set_lang
        else:
            return request.accept_languages.best_match(available_langs)


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


def register_blueprints(app):
    from colournaming.home.views import bp as home_module
    app.register_blueprint(home_module, url_prefix='/')
    from colournaming.namer.views import bp as namer_module
    app.register_blueprint(namer_module, url_prefix='/namer')


def setup_logging(app):
    if not app.debug:
        import logging
        from logging.handlers import RotatingFileHandler
        handler = RotatingFileHandler('colournaming.log', maxBytes=10000, backupCount=1)
        handler.setLevel(logging.INFO)
        app.logger.addHandler(handler)


def make_colour_namers(app):
    app.namers = instantiate_namers()
