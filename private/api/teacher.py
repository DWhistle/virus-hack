from flask import Blueprint

teacher_api = Blueprint("teacher", __name__, url_prefix="/teacher")

@teacher_api.route("/", methods = ["GET"])
def get_teachers():
    return {"teachers": 123}