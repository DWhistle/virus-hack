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