from sqlalchemy.sql.schema import Column, ForeignKey, MetaData
from sqlalchemy.types import Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from private.db.models import init_session

meta = MetaData()
Base = declarative_base(metadata=meta)

class Class(Base):
    __tablename__ = 'class'
    id = Column(Integer, primary_key=True)
    grade = Column(Integer)
    specialization = Column(String(40))
    roles = Column(Integer, ForeignKey("role.id"))

class Role(Base):
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    mask = Column(Integer)

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

class Session(Base):
    __tablename__ = 'session'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    key = Column(String(127))
    def check_identity(self):
        pass

class DbMethods:
    @staticmethod
    def user_info_by_id(user_id: int):
        info = []
        with init_session() as ss:
            rs = ss.query(User, Profile)\
                .filter(User.id == Profile.user_id)\
                    .filter(User.id == user_id).first()
        return rs
