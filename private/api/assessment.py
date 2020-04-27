from flask import Blueprint, request
from flask.helpers import send_file
import io

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
