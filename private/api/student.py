from flask import Blueprint

student_api = Blueprint("student", __name__, url_prefix="/student")

@student_api.route("/", methods = ["GET"])
def get_students():
    return {"students": 123}