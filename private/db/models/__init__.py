from .identity import User, Session
from .students import Student
from .teachers import Teacher

from sqlalchemy import create_engine
from private.config import db

db_connection = create_engine(f"{db['driver']}://{db['user']}:{db['password']}@localhost/{db['database']}")
