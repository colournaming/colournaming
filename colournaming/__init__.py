from flask import Flask, render_template, request
from flask_babel import Babel
from config import LANGUAGES


app = Flask(__name__)
# if 'COLOURNAMING_CFG' in os.environ:
    # app.config.from_envvar('COLOURNAMING_CFG')
# else:
    # app.config.from_object('colournaming.default_config')
babel = Babel(app)


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(LANGUAGES.keys())


@app.errorhandler(404)
def not_found(error):
        return render_template('404.html'), 404


@app.errorhandler(401)
def permission_denied(error):
        return render_template('401.html'), 401


from colournaming.home.views import bp as home_module
app.register_blueprint(home_module)
