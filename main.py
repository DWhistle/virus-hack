from flask import Flask

from private.config import configure_resources
configure_resources()
from private.service import api
from private.api.user import user_api
from private.api.teacher import teacher_api
from private.api.calendar import calendar_api
from private.api.assessment import assessment_api

app = Flask(__name__)
app.register_blueprint(user_api)
app.register_blueprint(teacher_api)
app.register_blueprint(calendar_api)
app.register_blueprint(assessment_api)


@app.route("/")
def hw():
    return {"123": "123"}


@app.route('/api/info')
def info():
    return api.get_info()


if __name__ == '__main__':
    app.run("0.0.0.0", port=5000)
