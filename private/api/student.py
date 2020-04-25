from flask import Blueprint
from private.db.models import Student

student_api = Blueprint("student", __name__, url_prefix="/student")

@student_api.route("/", methods = ["GET"])
def get_students():
    student = Student()
    return {"students": student.get_all()}