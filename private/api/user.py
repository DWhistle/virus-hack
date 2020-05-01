from flask import Blueprint, request
from private.db.models.identity import DbMethods
from . import RegistrationForm, ValidationError, ApiException
import hashlib

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
    if not form.validate():
        raise ValidationError("Ошибка валидации!", status_code=400)
    try:
        user_id = DbMethods.register_user(form.name.data, form.email.data, 
                            hashlib.sha256(form.password.data.encode('utf-8')).digest(),
                            form.age.data, form.phone.data,
                            form.gender.data, form.class_id.data)
        return {
            "user_id": user_id,
            "status": True
        }
    except Exception as e:
        raise ApiException(repr(e), 500)

@user_api.errorhandler(ApiException)
def handle_invalid_usage(error):
    return error.json