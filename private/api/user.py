from flask import Blueprint, request
from private.db.models.identity import DbMethods
from . import RegistrationForm, ValidationError, ApiException
import hashlib
from private.service.auth import Registration, TokenAuth, UserValidation, require_role
from private.api.forms import LoginForm
import random

user_api = Blueprint("user", __name__, url_prefix="/user")

@user_api.route("/<id>", methods = ["GET"])
def get_by_id(id):
    id = int(id or 0) 
    user, profile = DbMethods.user_info_by_id(id)
    return {"id": user.id,
            "name": user.name,
            "class_id": user.class_id,
            "age": profile.age,
            "gender": profile.gender,
            "phone": profile.phone,
            "email": profile.email,
            "birthday": profile.birthday}

@user_api.route("/my", methods = ["GET"])
@require_role
def get_current_user_id(identity):
    user, profile = DbMethods.user_info_by_id(identity.user_id)
    user_class = DbMethods.class_by_id(user.class_id)
    return {"id": user.id,
            "name": user.name,
            "class_id": user.class_id,
            "class_name": user_class.name,
            "age": profile.age,
            "gender": profile.gender,
            "phone": profile.phone,
            "email": profile.email,
            "birthday": profile.birthday}

@user_api.route("/", methods = ["GET"])
def get_all():
    rs = DbMethods.user_info_all()
    users = []
    for user, profile in rs:
        users.append({"id": user.id,
            "name": user.name,
            "age": profile.age,
            "gender": profile.gender,
            "phone": profile.phone,
            "email": profile.email,
            "birthday": profile.birthday,
            "is_connected": True if random.randint(0,1) else False})
    return {"users": users * 2}

@user_api.route("/register", methods = ["POST"])
def register_user():
    form = RegistrationForm(request.form)
    if not form.validate():
        raise ValidationError("Ошибка валидации!", status_code=400)
    try:
        registration = Registration()
        user_id = registration.register_user(form.name.data, form.email.data, 
                            form.password.data,
                            form.age.data, form.phone.data,
                            form.gender.data, form.class_id.data, form.username.data)
        return {
            "user_id": user_id,
            "status": True
        }
    except Exception as e:
        raise ApiException(repr(e), 500)

@user_api.route("/login", methods = ["POST"])
def login():
    form = LoginForm(request.form)
    if not form.validate():
        raise ValidationError("Ошибка валидации!", status_code=400)
    validation = UserValidation()
    try:
        user_id, class_id = validation.check_identity(form.username.data, form.password.data)
    except Exception as e:
        raise ApiException(repr(e), 500)
    auth = TokenAuth()
    token = auth.create_auth_token(user_id, class_id)
    return {
        "status": True,
        "token": token
    }

@user_api.errorhandler(ApiException)
def handle_invalid_usage(error):
    return error.json