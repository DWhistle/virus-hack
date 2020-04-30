from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.types import Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from .identity import Base

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

class Lesson(Base):
    __tablename__ = 'lesson'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))

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
    def lesson_add(name: str):
        from private.db.models import init_session
        info = []
        with init_session() as ss:
            ss.add_all([Lesson(name=name)])
            ss.commit()
