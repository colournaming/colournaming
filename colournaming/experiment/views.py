"""Views for the experiment."""

from flask import Blueprint, jsonify, redirect, render_template, session, url_for
from . import forms

bp = Blueprint('experiment', __name__)


def check_in_experiment():
    """Redirect to the start of the experiment if the session is not initialized."""
    if 'experiment' not in session:
        return redirect(url_for('experiment.start'))


@bp.route('/')
def start():
    """Show the experiment start page."""
    session['experiment'] = {}
    return redirect(url_for('experiment.display_properties'))


@bp.route('/display_properties.html', methods=['GET', 'POST'])
def display_properties():
    """Show the display properties form and handle responses."""
    check_in_experiment()
    form = forms.DisplayForm()
    if form.validate_on_submit():
        session['experiment']['display'] = {
            'greyscale_levels': form.levels.data,
            'screen_width': form.screen_width.data,
            'screen_height': form.screen_height.data
        }
        return redirect(url_for('experiment.colour_vision'))
    return render_template('display_properties.html', form=form)


@bp.route('/colour_vision.html', methods=['GET', 'POST'])
def colour_vision():
    """Show the colour vision test and handle responses."""
    check_in_experiment()
    form = forms.ColourVisionForm()
    if form.validate_on_submit():
        session['experiment']['vision'] = {
            'colour_vision_complete': form.tests_complete.data,
            'colour_vision_correct': form.tests_correct.data
        }
        return jsonify(success=True, url=url_for('experiment.name_colour'))
    return render_template('colour_vision.html', form=form)


@bp.route('/name_colour.html')
def name_colour():
    """Show the name colour form and handle responses."""
    check_in_experiment()
    print(session)
    form = forms.ColourNameForm()
    if form.validate_on_submit():
        print('log data')
    return render_template('name_colour.html', form=form)


@bp.route('/observer_information.html')
def observer_information():
    """Show the observer information form and handle responses."""
    check_in_experiment()
    form = forms.ObserverInformationForm()
    if form.validate_on_submit():
        session['experiment']['observer-age'] = form.age.data
        session['experiment']['observer-gender'] = form.gender.data
        session['experiment']['observer-colour_experience'] = form.colour_experience.data
        session['experiment']['observer-language_experience'] = form.language_experience.data
        session['experiment']['observer-education_level'] = form.education_level.data
        session['experiment']['observer-user_agent'] = form.user_agent.data
        session['experiment']['observer-country_raised'] = form.country_raised.data
        session['experiment']['observer-country_resident'] = form.country_resident.data
        return redirect(url_for('experiment.thankyou'))
    return render_template('observer_information.html', form=form)


@bp.route('/thankyou.html')
def thankyou():
    """Show the thankyou for participation page."""
    return render_template('thankyou.html')