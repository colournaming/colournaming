"""Views for the experiment."""

from flask import Blueprint, redirect, render_template, url_for
from . import forms

bp = Blueprint('experiment', __name__)


@bp.route('/')
def start():
    """Show the experiment start page."""
    return redirect(url_for('experiment.display_properties'))


@bp.route('/display_properties.html', methods=['GET', 'POST'])
def display_properties():
    form = forms.GreyscaleLevelsForm()
    if form.validate_on_submit():
        return redirect(url_for('experiment.colour_vision'))
    return render_template('display_properties.html', form=form)


@bp.route('/colour_vision.html')
def colour_vision():
    return render_template('colour_vision.html')
