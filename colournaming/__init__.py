"""Website for the colournaming experiment."""

import click
from flask import Flask, render_template, request, current_app, session
from flask_babel import Babel
import pytest
from sqlalchemy.exc import ProgrammingError
import user_agents
from . import admin
from .database import db
from .email import mail
from .experimentcol.controller import read_targets_from_file as read_col_targets_from_file
from .experimentcolbg.controller import (
    read_backgrounds_from_file,
    read_targets_from_file as read_colbg_targets_from_file,
)
from .mturk.controller import list_mturk_tasks
from .namer.controller import read_centroids_from_file, instantiate_namers


def create_app():
    """Create an instance of the app."""
    app = Flask(__name__)
    app.config.from_envvar("COLOURNAMING_CFG")
    db.init_app(app)
    mail.init_app(app)
    Babel(app, locale_selector=get_locale)
    set_error_handlers(app)
    setup_logging(app)
    setup_cli(app)
    set_before_request(app)
    register_blueprints(app)
    make_colour_namers(app)
    return app


def get_locale():
    available_langs = [x["code"] for x in current_app.config.get("LANGUAGES")]
    requested_lang = session.get("interface_language", None)
    if requested_lang in available_langs:
        locale = requested_lang
    else:
        locale = request.accept_languages.best_match(available_langs)
    return locale


def set_before_request(app):
    @app.before_request
    def before_req():
        agent_string = request.headers.get("User-Agent", "")
        try:
            ua = user_agents.parse(agent_string)
        except TypeError:
            request.mobile = False
        else:
            request.mobile = ua.is_mobile


def set_error_handlers(app):
    @app.errorhandler(404)
    def not_found(error):
        return render_template("404.html"), 404

    @app.errorhandler(401)
    def permission_denied(error):
        return render_template("401.html"), 401


def setup_cli(app):
    @app.cli.command()
    @click.argument("centroids_file", type=click.File("r"))
    @click.argument("language_name")
    @click.argument("language_code")
    def import_centroids(centroids_file, language_name, language_code):
        """Import a centroids file into the database."""
        read_centroids_from_file(centroids_file, language_name, language_code)

    @app.cli.command()
    @click.argument("filename", type=click.File("w"))
    def export_responses(filename):
        """Export responses to CSV."""
        admin.controller.get_responses(filename)

    @app.cli.command()
    @click.argument("filename", type=click.File("w"))
    def export_participants(filename):
        """Export participants to CSV."""
        admin.controller.get_participants(filename)

    @app.cli.command()
    @click.argument("filename", type=click.File("w"))
    def export_agreements(filename):
        """Export agreements to CSV."""
        admin.controller.get_agreements(filename)

    @app.cli.command()
    @click.argument("targets_file", type=click.File("r"))
    def import_col_targets(targets_file):
        """Import a targets file into the database."""
        read_col_targets_from_file(targets_file)

    @app.cli.command()
    @click.argument("targets_file", type=click.File("r"))
    @click.option("--delete-existing", is_flag=True)
    def import_colbg_targets(targets_file, delete_existing):
        """Import a targets file into the database."""
        read_colbg_targets_from_file(targets_file, delete_existing=delete_existing)

    @app.cli.command()
    @click.argument("backgrounds_file", type=click.File("r"))
    @click.option("--delete-existing", is_flag=True)
    def import_colbg_backgrounds(backgrounds_file, delete_existing):
        """Import a targets file into the database."""
        read_backgrounds_from_file(backgrounds_file, delete_existing=delete_existing)

    @app.cli.command()
    @click.argument("filename", type=click.File("w"))
    def export_colbg_responses(filename):
        """Export coloured background responses to CSV."""
        admin.controller.get_colbg_responses(filename)

    @app.cli.command()
    @click.argument("filename", type=click.File("w"))
    def export_colbg_participants(filename):
        """Export coloured background participants to CSV."""
        admin.controller.get_colbg_participants(filename)

    @app.cli.command()
    @click.argument("filename", type=click.File("w"))
    def export_mturk_responses(filename):
        """Export coloured background responses to CSV."""
        admin.controller.get_mturk_responses(filename)

    @app.cli.command()
    @click.argument("filename", type=click.File("w"))
    def export_mturk_participants(filename):
        """Export coloured background participants to CSV."""
        admin.controller.get_mturk_participants(filename)

    @app.cli.command()
    def mturk_tasks():
        """List completed Mechanical Turk tasks."""
        completed_tasks = list_mturk_tasks()
        print("completion_id,response_count")
        for task in completed_tasks:
            print(task.completion_id, len(task.participant.responses), sep=",")

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
        pytest.main(["tests"])

    @app.cli.command()
    @click.pass_context
    def help(ctx):
        """Show help message."""
        print(ctx.parent.get_help())


def register_blueprints(app):
    from colournaming.home.views import bp as home_module
    from colournaming.namer.views import bp as namer_module
    from colournaming.experimentcol.views import bp as experimentcol_module
    from colournaming.experimentcolbg.views import bp as experimentcolbg_module
    from colournaming.admin.views import bp as admin_module
    from colournaming.mturk.views import bp as mturk_module

    app.register_blueprint(home_module, url_prefix="/")
    app.register_blueprint(namer_module, url_prefix="/namer")
    app.register_blueprint(experimentcol_module, url_prefix="/experimentcol")
    app.register_blueprint(experimentcolbg_module, url_prefix="/experimentcolbg")
    app.register_blueprint(admin_module, url_prefix="/admin")
    app.register_blueprint(mturk_module, url_prefix="/mturk")


def setup_logging(app):
    if not app.debug:
        import logging
        from logging.handlers import RotatingFileHandler

        handler = RotatingFileHandler("colournaming.log", maxBytes=10000, backupCount=1)
        handler.setLevel(logging.INFO)
        app.logger.addHandler(handler)


def make_colour_namers(app):
    with app.app_context():
        try:
            app.namers = instantiate_namers()
        except ProgrammingError:
            pass


def lang_is_rtl(locale):
    return locale.language in ("ar", "he", "ckb", "fa", "ur")
