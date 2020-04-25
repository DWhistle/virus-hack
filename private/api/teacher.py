from flask import Blueprint
from private.db.models import Teacher

teacher_api = Blueprint("teacher", __name__, url_prefix="/teacher")

@teacher_api.route("/", methods = ["GET"])
def get_students():
    teacher = Teacher()
    return {"teachers": teacher.get_all()}