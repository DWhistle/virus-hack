
from flask import Blueprint, request
from private.db.models import Event, Profile, init_session, User
from datetime import datetime
from datetime import timedelta
from private.db.models.education import Lesson

calendar_api = Blueprint("calendar", __name__, url_prefix="/calendar")

@calendar_api.route("/", methods = ["GET"])
def get_by_id():
    teacher_id = int(request.args.get('teacher_id') or 0)
    class_id = int(request.args.get('class_id') or 0)
    id = int(request.args.get('id') or 0)
    events = []
    with init_session() as ss:
        q = ss.query(Event, User, Lesson)
        if id:
            q.filter(Event.id == id)
        if class_id:
            q.filter(Event.class_id == class_id)
        if teacher_id:
            q.filter(Event.id == teacher_id)
        q.filter(User.id == Event.teacher_id)
        q.filter(Lesson.id == Event.lesson_id)
        rs = q.all()
    for event, user, lesson in rs:
        events.append(
            {"id": event.id,
             "teacher_name": user.name,
             "lesson": lesson.name,
             "description": event.description,
             "begin_time": event.begin_time,
             "end_time": event.end_time,
             "homework": "12345"})

    return {"lessons": events}

def get_by_id():
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