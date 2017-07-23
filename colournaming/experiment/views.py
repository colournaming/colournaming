"""Views for the experiment."""

from flask import Blueprint, jsonify, redirect, render_template, request, session, url_for
from . import forms
from . import controller

bp = Blueprint('experiment', __name__)


def check_in_experiment():
    if 'experiment' not in session:
        return redirect(url_for('experiment.start'))


@bp.route('/')
def start():
    """Show the experiment start page."""
    session['experiment'] = {}
    return redirect(url_for('experiment.display_properties'))


@bp.route('/display_properties.html', methods=['GET', 'POST'])
def display_properties():
    check_in_experiment()
    form = forms.GreyscaleLevelsForm()
    if form.validate_on_submit():
        session['experiment']['greyscale_levels'] = form.levels
        return redirect(url_for('experiment.colour_vision'))
    return render_template('display_properties.html', form=form)


@bp.route('/colour_vision.html', methods=['GET', 'POST'])
def colour_vision():
    check_in_experiment()
    form = forms.ColourVisionForm()
    if form.validate_on_submit():
        session['experiment']['colour_vision_complete'] = form.tests_complete.data
        session['experiment']['colour_vision_correct'] = form.tests_correct.data
        return jsonify(success=True, url=url_for('experiment.name_colour'))
    return render_template('colour_vision.html', form=form)


@bp.route('/name_colour.html')
def name_colour():
    check_in_experiment()
    print(session)
    form = forms.ColourNameForm()
    if form.validate_on_submit():
        print('log data')
    return render_template('name_colour.html', form=form)


@bp.route('/observer_information.html')
def observer_information():
    check_in_experiment()
    form = forms.ObserverInformationForm()
    if form.validate_on_submit():
        return redirect(url_for('experiment.thankyou'))
    return render_template('observer_information.html', form=form)


@bp.route('/thankyou.html')
def thankyou():
    return render_template('thankyou.html')
