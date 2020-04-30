from wtforms import StringField, PasswordField, IntegerField, Form, BooleanField
from wtforms import validators

class RegistrationForm(Form):
    name = StringField('name', [validators.Length(min=4, max=100)])
    email = StringField('email', [validators.Length(min=6, max=35)])
    password = PasswordField('password', [
        validators.DataRequired(),
    ])
    age = IntegerField('age', validators=[validators.NumberRange(7, 80, "Возраст невалиден")])
    accept_tos = BooleanField('agreement', [validators.DataRequired()])
    phone = StringField('phone', validators=[validators.Length(11, 11, "Невалидный номер телефона")])
    gender = IntegerField('gender', validators=[validators.NumberRange(0,2)])