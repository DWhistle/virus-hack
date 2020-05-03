from wtforms import StringField, PasswordField, IntegerField, FieldList, Form, BooleanField
from wtforms import validators
from wtforms import FormField
from wtforms import DateTimeField

class RegistrationForm(Form):
    name = StringField('Name', [validators.Length(min=4, max=100), validators.DataRequired()])
    email = StringField('Email', [validators.Length(min=6, max=35), validators.DataRequired()])
    password = PasswordField('Password', [
        validators.DataRequired(),
    ])
    username = StringField('Username', [validators.Length(min=6, max=35), validators.DataRequired()])
    age = IntegerField('Age', validators=[validators.NumberRange(7, 80, "Возраст невалиден"), validators.DataRequired()])
    accept_agr = BooleanField('Agreement', [validators.DataRequired()])
    phone = StringField('Phone', validators=[validators.Length(11, 11, "Невалидный номер телефона")])
    gender = IntegerField('Gender', validators=[validators.NumberRange(0,2)])
    class_id = IntegerField('Class', validators=[validators.DataRequired()])

class LoginForm(Form):
    username = StringField('Username', validators=[validators.DataRequired()])
    password = PasswordField('Password', [
        validators.DataRequired(),
    ])

class TaskForm(Form):
    task_name = StringField('Name', validators=[validators.DataRequired()])
    lesson_id = IntegerField('LessonId', validators=[validators.DataRequired()])
    assignment = StringField('Assignment', validators=[validators.DataRequired()])
    assignment_type = StringField('AssignmentType', validators=[validators.DataRequired()])

class AssignmentForm(Form):
    teacher_id = IntegerField('TeacherId')
    assignee_user_id = IntegerField('AssigneeUserId', validators=[validators.DataRequired()])
    task_id = IntegerField('TaskId', validators=[validators.DataRequired()])
    event_id = IntegerField('EventId', validators=[validators.DataRequired()])


class PinForm(Form):
    assignment_id  = IntegerField('AssignmentId', validators=[validators.DataRequired()])
    coord_x = IntegerField('CoordX', validators=[validators.DataRequired()])
    coord_y = IntegerField('CoordY', validators=[validators.DataRequired()])
    message = StringField('Message', validators=[validators.DataRequired()])

class PinsForm(Form):
    pins = FieldList(FormField(PinForm))


class EventForm(Form):
    teacher_id = IntegerField('TeacherId', validators=[validators.DataRequired()])
    lesson_id = IntegerField('LessonId', validators=[validators.DataRequired()])
    class_id = IntegerField('ClassId', validators=[validators.DataRequired()])
    description = StringField('Description', validators=[validators.DataRequired()])
    begin_time = DateTimeField('Begin', validators=[validators.DataRequired()])
    end_time = DateTimeField('End', validators=[validators.DataRequired()])