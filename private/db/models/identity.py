from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.types import Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Class(Base):
    __tablename__ = 'class'
    id = Column(Integer, primary_key=True)
    grade = Column(Integer)
    specialization = Column(String(40))
    roles = Column(Integer)

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(127))
    username = Column(String(32))
    password = Column(String(255))
    class_id = Column(Integer, ForeignKey('class.id'))

    @staticmethod
    def get_info():
        pass

class Profile(Base):
    __tablename__ = 'profile'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    age = Column(Integer)
    gender = Column(Integer)
    phone = Column(String(11))
    email = Column(String(256))
    birthday = Column(Date())

class Session:

    def check_identity(self):
        pass