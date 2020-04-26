from .identity import User, Session, Class
from .students import Student
from .teachers import Teacher

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from private.config import db

db_connection = create_engine(f"{db['driver']}://{db['user']}:{db['password']}@localhost/{db['database']}")
