from flask import Flask

from private.config import configure_resources
from private.service import api


app = Flask(__name__)

@app.route("/")
def hw():
    return {"123": "123"}


@app.route('/api/info')
def info():
    return api.get_info()


if __name__ == '__main__':
    configure_resources()
    app.run("0.0.0.0", port=5000)
