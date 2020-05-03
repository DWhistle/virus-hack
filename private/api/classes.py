from flask import Blueprint
from private.db.models.identity import Class, DbMethods

classes_api = Blueprint("classes", __name__, url_prefix="/classes")


@classes_api.route("/members", methods = ["GET"])
def get_class_members():
    pass

@classes_api.route("/add", methods = ["POST"])
def create_class():
    pass

@classes_api.route("/add", methods = ["POST"])
def get_classes():
    rs = DbMethods.get_all_classes()
    classes = []
    for class_e, role in rs:
        classes.append({
                "id": class_e.id,
                "grade": class_e.grade,
                "specialization": class_e.specialization,
                "role": role.name,
                "role_id": role.id})
    return classes
