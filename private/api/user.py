from flask import Blueprint, request
from private.db.models.identity import DbMethods
from . import RegistrationForm


user_api = Blueprint("user", __name__, url_prefix="/user")

@user_api.route("/<id>", methods = ["GET"])
def get_by_id(id):
    id = int(id or 0) 
    user, profile = DbMethods.user_info_by_id(id)
    return {"id": user.id,
            "name": user.name,
            "age": profile.age,
            "gender": profile.gender,
            "phone": profile.phone,
            "email": profile.email,
            "birthday": profile.birthday}

@user_api.route("/register", methods = ["POST"])
def register_user():
    form = RegistrationForm(request.form)
    