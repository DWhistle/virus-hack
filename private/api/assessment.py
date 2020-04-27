from flask import Blueprint, request
from flask.helpers import send_file
import io
from PIL import Image

assessment_api = Blueprint("assessment", __name__, url_prefix="/assessment")

@assessment_api.route("/", methods = ["GET"])
def get_by_id():
    id = int(request.args.get('id') or 0)
    f_name = f"../pictures/{id}.jpg"
    image_binary = Image.open(f_name)
    return send_file(
    io.BytesIO(image_binary),
    mimetype='image/jpeg',
    as_attachment=True,
    attachment_filename=f_name)