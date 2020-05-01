from flask import Blueprint
from private.service import require_role
from private.api import ApiException
from private.db.models.education import DbMethods
teacher_api = Blueprint("teacher", __name__, url_prefix="/teacher")

@teacher_api.route("/", methods = ["GET"])
@require_role
def get_teachers(user_id: int):
    return {"teachers": 123}

@teacher_api.route('/lessons', methods = ["GET"])
def get_lessons():
    from private.db.models import init_session
    rs = DbMethods.lessons_get_all()
    return {"lessons":
        map(lambda l: {"id": l.id, "name": l.name}, rs)}


@teacher_api.errorhandler(ApiException)
def handle_invalid_usage(error):
    return error.json