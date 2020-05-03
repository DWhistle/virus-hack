import unittest
from private.db.models import Profile, User, Event, Class, init_session, Lesson
import datetime
from datetime import datetime
from datetime import timedelta
from random import randint
from private.db.models.identity import Role

class TestEdu(unittest.TestCase):

    def add_multiple_calendars(self):
        with init_session() as ss:
            for i in range(2, 10):
                day = randint(1, 7)
                event = Event(id=i,teacher_id=1,lesson_id=1,
                class_id=1,description='Урок ' + str(i), 
                begin_time = datetime.now() + timedelta(days=day),
                end_time = datetime.now() + timedelta(days=day) + timedelta(minutes=40))
                ss.add(event)

    def test_db_tables(self):
        def_class = Class(id=1, grade=1, roles=123, specialization='A')
        def_user = User(id=1, name = "Ольга Петровна", username='123', password='123', class_id = 1)
        def_profile = Profile(id=1,user_id=1,age=23,gender=1,phone='123213',email='sdsds@sds', birthday=datetime.now())
        def_lesson = Lesson(id=1,name="Математика")
        def_event = Event(id=1,teacher_id=1,lesson_id=1,
        class_id=1,description='Урок1', 
        begin_time = datetime.now() + timedelta(days=3),
        end_time = datetime.now() + timedelta(days=3) + timedelta(minutes=40))
        with init_session() as ss:
            ss.add(def_class)
        with init_session() as ss:
            ss.add(def_user)
        with init_session() as ss:
            ss.add(def_profile)
            ss.add(def_lesson)
        with init_session() as ss:
            ss.add(def_event)

    def add_classes_and_roles(self):
        teacher_role = Role(name = "Учитель", mask=2)
        director_role = Role(name = "Директор", mask=3)
        student_role = Role(name = "Ученик", mask=4)
        with init_session() as ss:
            ss.add(teacher_role)
            ss.add(director_role)
            ss.add(student_role)
            ss.fetch()
            teacher_class = Class(grade=100, roles=teacher_role.id, specialization='Учитель математики')
            student_class = Class(grade=6, roles=student_role.id, specialization='6-Б класс')
            director_class = Class(grade=242423123, roles=teacher_role.id, specialization='Директор школы')
            ss.add(teacher_class)
            ss.add(student_class)
            ss.add(director_class)


