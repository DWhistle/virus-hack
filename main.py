from flask import Flask

from private.config import Configurator
Configurator.configure_resources()
from private.api.user import user_api
from private.api.teacher import teacher_api
from private.api.calendar import calendar_api
from private.api.assessment import assessment_api
from private.api.dashboard import dashboard_api
from private.api.classes import classes_api
from flask_cors import CORS
app = Flask(__name__)
app.config['SECRET'] = Configurator.app_config['secret']
CORS(app)
app.register_blueprint(user_api)
app.register_blueprint(teacher_api)
app.register_blueprint(calendar_api)
app.register_blueprint(assessment_api)
app.register_blueprint(dashboard_api)
app.register_blueprint(classes_api)



if __name__ == '__main__':
    app.run("0.0.0.0", port=5000)
