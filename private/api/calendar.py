
from flask import Blueprint, request
from private.db.models import Event, Profile, init_session, User
from datetime import datetime
from datetime import timedelta
from private.db.models.education import Assignment, DbMethods, Lesson
from private.api.forms import EventForm
from private.api.assessment import get_assignment_with_pins

calendar_api = Blueprint("calendar", __name__, url_prefix="/calendar")

@calendar_api.route("/", methods = ["GET"])
def get_by_id():
    teacher_id = int(request.args.get('teacher_id') or 0)
    class_id = int(request.args.get('class_id') or 0)
    event_id = int(request.args.get('id') or 0)
    events = []
    with init_session() as ss:
        filters = []
        filters.append(User.id == Event.teacher_id)
        filters.append(Lesson.id == Event.lesson_id)
        filters.append(Assignment.event_id == Event.id)
        if event_id:
            filters.append(Event.id == event_id)
        if class_id:
            filters.append(Event.class_id == class_id)
        if teacher_id:
            filters.append(Event.id == teacher_id)
        rs = ss.query(Event, User, Lesson, Assignment).filter(*filters).all()
    for event, user, lesson, assignment in rs:
        events.append(
            {"id": event.id,
             "teacher_name": user.name,
             "lesson": lesson.name,
             "description": event.description,
             "begin_time": event.begin_time,
             "end_time": event.end_time,
             "homework": get_assignment_with_pins(assignment.id)
             }
        )

    return {"lessons": events}