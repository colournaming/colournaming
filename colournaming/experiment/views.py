"""Views for the experiment."""

from flask import Blueprint, jsonify, redirect, render_template, request, session, url_for
from flask_babel import lazy_gettext
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
    try:
        browser_language = request.accept_languages[0][0]
    except IndexError:
        browser_language = None
    session['experiment'] = {
        'client': {
            'user_agent': request.user_agent.string,
            'browser_language': browser_language
        },
        'response_count': 0
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
        }
        session['experiment']['participant_id'] = controller.save_participant(session['experiment'])
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
        print('colour vision form validated')
        session['experiment']['vision'] = {
            'square_disappeared': form.square_disappeared.data
        }
        session.modified = True
        print(session)
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
                'name': form.name.data,
                'response_time': form.response_time.data
            }
        )
        session['experiment']['response_count'] += 1
        session.modified = True
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
        print('observer information form validated')
        session['experiment']['observer'] = {
            'age': form.age.data,
            'gender': form.gender.data,
            'gender_other': form.gender_other.data,
            'colour_experience': form.colour_experience.data,
            'language_experience': form.language_experience.data,
            'education_level': form.education_level.data,
            'country_raised': form.country_raised.data,
            'country_resident': form.country_resident.data,
            'ambient_light': form.ambient_light.data,
            'screen_light': form.screen_light.data,
            'screen_temperature': form.screen_temperature.data,
            'screen_distance': form.screen_distance.data,
            'device': form.display_device.data
        }
        session.modified = True
        controller.update_participant(session['experiment'])
        return redirect(url_for('experiment.thankyou'))
    if form.errors:
        for field, error in form.errors.items():
            print(field, repr(getattr(form, field).data), error)
    return render_template('observer_information.html', form=form)


@bp.route('/thankyou.html')
def thankyou():
    """Show the thankyou for participation page."""
    try:
        response_count = session['experiment'].get('response_count', 0)
        perc = controller.response_count_percentage(response_count)
    except:
        perc = 0
    top_namers_msg = lazy_gettext('You are in the 0% top colour namers.')
    top_namers_msg = top_namers_msg.replace('0%', '{0:.0f}%'.format(perc))
    return render_template('thankyou.html', top_namers=top_namers_msg)
