
from flask import Blueprint
from private.db.models import Student
from datetime import datetime
from datetime import timedelta

calendar_api = Blueprint("calendar", __name__, url_prefix="/calendar")

@calendar_api.route("/<calendar_id>", methods = ["GET"])
def get_by_id(calendar_id):
   return {"lessons": [{
            "teacher_name": "Петрова Петя Петровна",
            "lesson": "Биология",
            "description": "урок с самостоялкой",
            "begin_time": datetime.now() + timedelta(days=1),
            "homework": "стр. 1, N 3,2,1,4",
            "end_time": datetime.now()+ timedelta(days=1) + timedelta(minutes=30)
        },
        {
            "teacher_name": "Петрова Ольга Викторовна",
            "lesson": "Русский",
            "description": "тупа урок",
            "begin_time": datetime.now() + timedelta(days=2),
            "homework": "стр. 14, N 3,2,1,4",
            "end_time": datetime.now()+ timedelta(days=2) + timedelta(minutes=30)
        }]}