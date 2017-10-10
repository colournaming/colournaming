"""Views for the experiment."""

from flask import Blueprint, jsonify, redirect, render_template, request, session, url_for
from . import controller, forms

bp = Blueprint('experiment', __name__)


def check_in_experiment():
    """Redirect to the start of the experiment if the session is not initialized."""
    if 'experiment' not in session:
        return redirect(url_for('experiment.start'))


@bp.route('/')
def start():
    """Show the experiment start page."""
    print('resetting experiment')
    session['experiment'] = {
        'client': {
            'ip_address': request.remote_addr,
            'user_agent': request.user_agent.string,
            'browser_language': request.accept_languages[0][0]
        }
    }
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
            'screen_height': form.screen_height.data,
            'screen_colour_depth': form.screen_colour_depth.data,
            'screen_distance': form.screen_distance.data,
            'ambient_light': form.ambient_light.data,
            'screen_light': form.screen_light.data
        }
        session.modified = True
        return redirect(url_for('experiment.colour_vision'))
    if form.errors:
        for field, error in form.errors.items():
            print(field, error)
    return render_template('display_properties.html', form=form)


@bp.route('/colour_vision.html', methods=['GET', 'POST'])
def colour_vision():
    """Show the colour vision test and handle responses."""
    check_in_experiment()
    form = forms.ColourVisionForm()
    if form.validate_on_submit():
        correct = float(form.tests_correct.data)
        complete = float(form.tests_complete.data)
        percent_tests_correct = int(100.0 * correct / complete)
        session['experiment']['vision'] = {
            'percent_correct': percent_tests_correct,
            'status': form.colour_vision_status.data
        }
        session['experiment']['participant_id'] = controller.save_participant(session['experiment'])
        session.modfied = True
        return jsonify({'success': True, 'url': url_for('experiment.name_colour')})
    if form.errors:
        for field, error in form.errors.items():
            print(field, error)
    return render_template('colour_vision.html', form=form)


@bp.route('/name_colour.html', methods=['GET', 'POST'])
def name_colour():
    """Show the name colour form and handle responses."""
    check_in_experiment()
    form = forms.ColourNameForm()
    if form.validate_on_submit():
        controller.save_response(
            session['experiment'],
            {
                'target_id': form.target_id.data,
                'name': form.name.data
            }
        )
    if form.errors:
        for field, error in form.errors.items():
            print(field, error)
    return render_template('name_colour.html', form=form)


@bp.route('/get_target.json')
def get_target():
    """Get a random colour target to name."""
    target = controller.get_random_target()
    return jsonify({
        'id': target.id,
        'r': target.red,
        'g': target.green,
        'b': target.blue
    }) 


@bp.route('/observer_information.html', methods=['GET', 'POST'])
def observer_information():
    """Show the observer information form and handle responses."""
    check_in_experiment()
    form = forms.ObserverInformationForm()
    if form.validate_on_submit():
        session['experiment']['observer'] = {
            'age': form.age.data,
            'gender': form.gender.data,
            'colour_experience': form.colour_experience.data,
            'language_experience': form.language_experience.data,
            'education_level': form.education_level.data,
            'country_raised': form.country_raised.data,
            'country_resident': form.country_resident.data
        }
        session.modified = True
        controller.update_participant(session['experiment'])
        return redirect(url_for('experiment.thankyou'))
    return render_template('observer_information.html', form=form)


@bp.route('/thankyou.html')
def thankyou():
    """Show the thankyou for participation page."""
    return render_template('thankyou.html')
