from private.config import configure_resources
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hw():
    return {"123": "123"}

if __name__ == '__main__':
    configure_resources()
    app.run("0.0.0.0", port=5000)
