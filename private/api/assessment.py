from flask import Blueprint, request
from flask.helpers import send_file
from private.service import require_role
from private.api.forms import TaskForm, AssignmentForm, PinsForm
from private.db.models.education import DbMethods
import io
import json

assessment_api = Blueprint("assessment", __name__, url_prefix="/assessment")

@assessment_api.route("/<id>", methods = ["GET"])
def get_by_id(id):
    id = int(id or 0)
    f_name = f"../pictures/{id}.jpg"
    return send_file(
    f_name,
    mimetype='image/jpeg',
    as_attachment=True)

@assessment_api.route("/pins/<id>", methods = ["GET"])
def pins_by_id(id):
    id = int(id or 0)
    return {"pins": 
    [(500,700, "вот тут поправить"),
    (550,800, "вот тут ещё")]}

@assessment_api.route("/task", methods=['PUT'])
@require_role
def add_task(identity):
    tf = TaskForm(request.form)
    task_id = DbMethods.task_add(tf.task_name.data,
                        tf.lesson_id.data,
                        tf.assignment.data,
                        tf.assignment_type.data)
    return {
        "task_id": task_id
    }

@assessment_api.route("/assignment", methods=['PUT'])
@require_role
def add_assignment(identity):
    af = AssignmentForm(request.form)
    assignment_id = DbMethods.assignment_add(identity.user_id,
                        af.assignee_class_id.data,
                        af.task_id.data)
    return {
        "task_id": assignment_id
    }

@assessment_api.route("/pins", methods=['PUT'])
@require_role
def add_pins(identity):
    return {
        "success": DbMethods.pins_add(request.get_json())
    }

@assessment_api.route("/assignment/<assignment_id>", methods=["GET"])
@require_role
def get_assignment_with_pins(identity, assignment_id):
    rs = DbMethods.get_full_assignment_info(assignment_id)
    print(rs)
    return {"pins": rs}