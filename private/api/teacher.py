from flask import Blueprint
from private.service import require_role
from private.api import ApiException
teacher_api = Blueprint("teacher", __name__, url_prefix="/teacher")

@teacher_api.route("/", methods = ["GET"])
@require_role
def get_teachers(user_id: int):
    return {"teachers": 123}



@teacher_api.errorhandler(ApiException)
def handle_invalid_usage(error):
    return error.json