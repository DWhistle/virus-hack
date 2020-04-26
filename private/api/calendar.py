
from flask import Blueprint, request
from private.db.models import Student, Event, Profile, Session
from datetime import datetime
from datetime import timedelta

calendar_api = Blueprint("calendar", __name__, url_prefix="/calendar")

@calendar_api.route("/<event>", methods = ["GET"])
def get_by_participators(event):
    # teacher_id = int(request.args.get('teacher_id') or 0)
    # class_id = int(request.args.get('class_id') or 0)

    # with Session() as ss:
    #     q = ss.query(Event, Profile)
    #     if teacher_id:
    #         q.filter(Profile.user_id == teacher_id)
    #     if class_id:
    #         q.filter(Event.class_id == class_id)
    #     events = q.all()
    # return {"lessons": events}

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