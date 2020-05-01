from wtforms import StringField, PasswordField, IntegerField, Form, BooleanField
from wtforms import validators

class RegistrationForm(Form):
    name = StringField('Name', [validators.Length(min=4, max=100), validators.DataRequired()])
    email = StringField('Email', [validators.Length(min=6, max=35), validators.DataRequired()])
    password = PasswordField('Password', [
        validators.DataRequired(),
    ])
    username = StringField('Username', [validators.Length(min=6, max=35), validators.DataRequired()])
    age = IntegerField('Age', validators=[validators.NumberRange(7, 80, "Возраст невалиден"), validators.DataRequired()])
    accept_agr = BooleanField('Agreement', [validators.DataRequired()])
    phone = StringField('Phone', validators=[validators.Length(11, 11, "Невалидный номер телефона"), validators.DataRequired()])
    gender = IntegerField('Gender', validators=[validators.NumberRange(0,2), validators.DataRequired()])
    class_id = IntegerField('Class', validators=[validators.DataRequired()])

class LoginForm(Form):
    username = StringField('Username', validators=[validators.DataRequired()])
    password = PasswordField('Password', [
        validators.DataRequired(),
    ])