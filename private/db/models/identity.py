from sqlalchemy.sql.schema import Column, ForeignKey, MetaData
from sqlalchemy.types import Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base

meta = MetaData()
Base = declarative_base(metadata=meta)

class Class(Base):
    __tablename__ = 'class'
    id = Column(Integer, primary_key=True)
    grade = Column(Integer)
    specialization = Column(String(40))
    roles = Column(Integer, ForeignKey("role.id"))

class AssignedClasses(Base):
    __tablename__ = 'assigned_classes'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    class_id = Column(Integer, ForeignKey('class.id'))


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

class UniversityRecommendation(Base):
    __tablename__ = 'university_recommendation'

    id = Column(Integer, primary_key=True)
    university = Column(String(127))
    specialization = Column(String(32))
    user_id = Column(Integer, ForeignKey('user.id'))

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
        from private.db.models import init_session
        info = []
        with init_session() as ss:
            rs = ss.query(User, Profile, UniversityRecommendation)\
                .filter(User.id == Profile.user_id)\
                    .filter(User.id == user_id) \
                    .filter(User.id == UniversityRecommendation.user_id).first()
        return rs

    @staticmethod
    def user_info_all():
        from private.db.models import init_session
        info = []
        with init_session() as ss:
            rs = ss.query(User, Profile)\
                .filter(User.id == Profile.user_id)\
                    .all()
        return rs
    
    @staticmethod
    def check_rights(class_id: int, role: str):
        from private.db.models import init_session
        with init_session() as ss:
            rs = ss.query(Class, Role) \
                .filter(Class.id == class_id) \
                    .filter(Class.roles == Role.id) \
                        .filter(Role.name == role).first()
            if not rs:
                from private.db.models import DbValueNotFoundError
                raise DbValueNotFoundError("Роли не существует!")

    @staticmethod
    def check_user_identity(username: str, password: str):
        from private.db.models import init_session
        with init_session() as ss:
            user = ss.query(User) \
                .filter(User.username == username, User.password == password).first()
        return user

    @staticmethod
    def role_by_id(role_id: int):
        from private.db.models import init_session
        info = []
        with init_session() as ss:
            rs = ss.query(Role) \
                    .filter(Role.id == role_id).first()
        return rs

    @staticmethod
    def class_by_id(class_id: int):
        from private.db.models import init_session
        info = []
        with init_session() as ss:
            rs = ss.query(Class, Role) \
                    .filter(Class.id == class_id) \
                    .filter(Class.roles == Role.id) \
                    .first()
        return rs

    @staticmethod
    def get_all_classes():
        from private.db.models import init_session
        with init_session() as ss:
            rs = ss.query(Class, Role) \
                    .filter(Class.roles == Role.id).all()
        return rs
        
    @staticmethod
    def register_user(name:str, email:str, password:str, age:int, phone:str, gender:int, class_id:int, username: str):
        from private.db.models import init_session
        with init_session() as ss:
            user = User(name=name, username=username, password=password, class_id=class_id)
            ss.add(user)
            ss.flush()
            profile = Profile(user_id=user.id, age=age, gender=gender, phone=phone, email=email)
            ss.add(profile)
        return user.id
            