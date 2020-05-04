from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.types import Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from .identity import Base
from private.db.models.identity import User

class Event(Base):
    __tablename__ = 'event'
    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer, ForeignKey('user.id'))
    lesson_id = Column(Integer, ForeignKey('lesson.id'))
    class_id = Column(Integer, ForeignKey('class.id'))
    description = Column(String(5000))
    begin_time = Column(DateTime())
    end_time = Column(DateTime())

    def get_by_id(self):
        pass

class Poll(Base):
    __tablename__ = 'poll'
    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer, ForeignKey("user.id"))
    class_id = Column(Integer, ForeignKey("user.class_id"))
    question = Column(String(500))
    answers = Column(String(120))
    poll_time = Column(DateTime)

class Lesson(Base):
    __tablename__ = 'lesson'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))

class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    lesson_id = Column(ForeignKey("lesson.id"))
    assignment = Column(String(1000))
    assignment_type = Column(String(40))
    

class Assignment(Base):
    __tablename__ = 'assignment'
    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer, ForeignKey("user.id"))
    assignee_user_id = Column(Integer, ForeignKey("user.id"))
    task_id  = Column(Integer, ForeignKey("task.id"))
    event_id = Column(Integer, ForeignKey("event.id"))
    mark = Column(Integer)

class Pin(Base):
    __tablename__ = 'pin'
    id = Column(Integer, primary_key=True)
    assignment_id  = Column(Integer, ForeignKey("assignment.id"))
    coord_x = Column(Integer)
    coord_y = Column(Integer)
    message = Column(String(500))

class DbMethods:
    @staticmethod
    def lesson_info_by_id(lesson_id: int):
        from private.db.models import init_session
        info = []
        with init_session() as ss:
            rs = ss.query(Lesson) \
                   .filter(Lesson.id == lesson_id).first()
        return rs
    
    @staticmethod
    def task_add(task_name: str, lesson_id: int, assignment: str, assignment_type: str):
        from private.db.models import init_session
        with init_session() as ss:
            task = Task(name=task_name, 
            lesson_id=lesson_id, 
            assignment=assignment, 
            assignment_type=assignment_type)
            ss.add(task)
        return task.id
    
    @staticmethod
    def assignment_add(teacher_id: int, assignee_class_id: int, assingment_id: int, event_id: int):
        from private.db.models import init_session
        with init_session() as ss:
            assignment = Assignment(teacher_id=teacher_id,
                                    assignee_user_id=assignee_class_id,
                                    task_id=assingment_id,
                                    event_id=event_id,
                                    mark=0)
            ss.add(assignment)
        return assignment.id


    @staticmethod
    def pins_add(pins: list):
        from private.db.models import init_session
        with init_session() as ss:
            for pin in pins:
                pin = Pin(assignment_id=pin['assignment_id'],
                        coord_x=pin['coord_x'],
                        coord_y=pin['coord_y'],
                        message=pin['message'])
                ss.add(pin)
        return True
    
    @staticmethod
    def get_full_assignment_info(assignment_id: int):
        from private.db.models import init_session
        with init_session() as ss:
            assignment, task = ss.query(Assignment, Task) \
            .filter(Assignment.task_id == Task.id) \
            .filter(Assignment.id == assignment_id).first()
            
            pins = ss.query(Pin) \
            .filter(Pin.assignment_id == assignment_id) \
            .all()
        return assignment, task, pins

    @staticmethod
    def lessons_get_all(lesson_id: int):
        from private.db.models import init_session
        info = []
        with init_session() as ss:
            rs = ss.query(Lesson) \
                   .filter(Lesson.id == lesson_id).all()
        return rs

    @staticmethod
    def lesson_add(name: str):
        from private.db.models import init_session
        info = []
        with init_session() as ss:
            ss.add_all([Lesson(name=name)])
            ss.commit()

    @staticmethod
    def lessons_for_student(user_id: int, class_id: int, event_id: int):
        from private.db.models import init_session
        filters = []
        filters.append(Event.class_id == class_id)
        filters.append(Lesson.id == Event.lesson_id)
        filters.append(User.id == Event.teacher_id)
        if event_id != 0:
            filters.append(Event.id == event_id)
            with init_session() as ss:
                assignments = ss.query(Assignment, Task) \
                    .filter(Assignment.event_id == event_id) \
                    .filter(Assignment.task_id == Task.id) \
                    .filter(Assignment.assignee_user_id == user_id).all()
        with init_session() as ss:
            rs = ss.query(Event, Lesson, User) \
                .filter(*filters).all()
        print(rs, assignments)
        return rs, assignments