"""Views for the namer."""

from flask import Blueprint, current_app, redirect, render_template, Response, session, url_for
from .controller import get_responses, get_participants
from .forms import LoginForm

bp = Blueprint('admin', __name__)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login page."""
    form = LoginForm()
    if form.validate_on_submit():
        print(form.password.data, current_app.config.get('ADMIN_PASSWORD'))
        if form.username.data == 'admin' and form.password.data == current_app.config.get('ADMIN_PASSWORD'):
            session['admin_logged_in'] = True
            return redirect(url_for('.index'))
    if form.errors:
        for field, error in form.errors.items():
            print(field, error)
    return render_template('login.html', form=form)


@bp.route('/')
def index():
    """Menu of admin functions."""
    if not session.get('admin_logged_in', False):
        return redirect(url_for('.login'))
    return render_template('admin_menu.html')


@bp.route('/responses.csv')
def show_responses():
    """Return experiment responses as CSV."""
    if not session.get('admin_logged_in', False):
        return redirect(url_for('.login'))
    return Response(get_responses(), mimetype='text/csv')


@bp.route('/participants.csv')
def show_participants():
    """Return participants as CSV."""
    if not session.get('admin_logged_in', False):
        return redirect(url_for('.login'))
    return Response(get_participants(), mimetype='text/csv')
