from flask import Blueprint
from private.db.models.identity import DbMethods

classes_api = Blueprint("classes", __name__, url_prefix="/classes")


@classes_api.route("/members", methods = ["GET"])
def get_class_members():
    pass

@classes_api.route("/add", methods = ["POST"])
def create_class():
    pass