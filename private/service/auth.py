from functools import wraps
from flask import request, current_app as app
from datetime import datetime, timedelta
from private.db.models.identity import DbMethods
import jwt
from private.db.models import DbValueNotFoundError

def require_role(func, role = ''):
    @wraps(func)
    def wrapped(*args, **kwargs):
        token = request.headers.get('Authorization', None)        
        auth = TokenAuth()
        try:
            user_id, class_id = auth.verify_token(auth.create_auth_token(1,2))
            auth.check_role(class_id, role)
        except DbValueNotFoundError as e:
            pass
        return func(user_id, *args, **kwargs)
    return wrapped

class TokenAuth:
    def create_auth_token(self, user_id: int, user_class_id: int):
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=0, hours=2),
                'iat': datetime.utcnow(),
                'sub': user_id,
                'class': user_class_id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET'),
                algorithm='HS256')
        except:
            raise

    def verify_token(self, token):
        try:
            payload = jwt.decode(token, app.config.get('SECRET'))
            return payload['sub'], payload['class']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def check_role(self, user_id, role):
        DbMethods.check_rights(user_id, role)
