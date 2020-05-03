
from flask import Blueprint, request
from private.db.models import Event, Profile, init_session, User
from datetime import datetime
from datetime import timedelta
from private.db.models.education import Assignment, DbMethods, Lesson
from private.api.forms import EventForm

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
        if event_id:
            filters.append(Event.id == event_id)
        if class_id:
            filters.append(Event.class_id == class_id)
        if teacher_id:
            filters.append(Event.id == teacher_id)
        rs = ss.query(Event, User, Lesson).filter(*filters).all()
    for event, user, lesson in rs:
        events.append(
            {"id": event.id,
             "teacher_name": user.name,
             "lesson": lesson.name,
             "description": event.description,
             "begin_time": event.begin_time,
             "end_time": event.end_time,
             "homework": "Страница 1, з. 2"
             })

    return {"lessons": events}


@calendar_api.route("/student/<event_id>", methods = ["GET"])
def get_lesson_for_student(identity, event_id):
    events = []
    assignments = []
    rs, tasks = DbMethods.lessons_for_student(identity.user_id, identity.class_id, event_id)
    for user, event, lesson in rs:
        events.append(
            {"id": event.id,
             "teacher_name": user.name,
             "lesson": lesson.name,
             "description": event.description,
             "begin_time": event.begin_time,
             "end_time": event.end_time,
             "homework": "Страница 1, з. 2"
             })
    if len(events) == 1 and tasks is not None:
        for assignment, task in tasks:
            assignments.append(
                {"lesson_id": task.lesson_id,
                "assignment": task.assignment,
                "assignment_type": task.assignment_type,
                "teacher_id": assignment.teacher_id,
                "assignee_user_id": assignment.assignee_user_id,
                "task_id": assignment.task_id,
                "mark": assignment.mark}
                )
        lesson['assignments'] = assignments
        return {"lesson": lesson}
    return {"lessons": events}