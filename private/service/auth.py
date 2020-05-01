from functools import wraps
from flask import request, current_app as app
from datetime import datetime, timedelta
from private.db.models.identity import DbMethods
import jwt
from private.db.models import DbValueNotFoundError
import hashlib
from private.api import ValidationError

def require_role(func, role = ''):
    @wraps(func)
    def wrapped(*args, **kwargs):
        token = request.headers.get('Authorization', None)        
        auth = TokenAuth()
        validation = UserValidation()
        try:
            user_id, class_id = auth.verify_token(token)
            validation.check_role(class_id, role)
        except (DbValueNotFoundError, jwt.ExpiredSignatureError, jwt.InvalidTokenError, jwt.DecodeError) as e:
            raise ValidationError((str(e), 401))
        return func(user_id, *args, **kwargs)
    return wrapped

def encode_password(password: str):
    return str(hashlib.sha256(password.encode('utf-8')).digest())


class UserValidation:
    def check_role(self, user_id, role):
        DbMethods.check_rights(user_id, role)

    def check_identity(self, username:str, password:str):
        user = DbMethods.check_user_identity(username, encode_password(password))
        if not user:
             raise Exception("пользователь не существует")
        return user.id, user.class_id

class Registration:
    def register_user(self, name:str, email:str, password:str, age:int, phone:str, gender:int, class_id:int, username: str):
        user_id = DbMethods.register_user(name, email, 
                            encode_password(password),
                            age, phone,
                            gender, class_id, username)
        return user_id

class TokenAuth:
    def create_auth_token(self, user_id: int, user_class_id: int):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, hours=2),
            'iat': datetime.utcnow(),
            'sub': user_id,
            'class': user_class_id
        }
        return jwt.encode(
            payload,
            app.config.get('SECRET'),
            algorithm='HS256').decode("utf-8")

    def verify_token(self, token):
            payload = jwt.decode(token, app.config.get('SECRET'))
            return payload['sub'], payload['class']