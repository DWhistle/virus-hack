from .identity import User, Session, Class, Profile
from .education import Event, Lesson

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from private.config import Configurator
from sqlalchemy.orm.session import sessionmaker
from contextlib import contextmanager

db = Configurator.db
db_connection = create_engine(f"{db['driver']}://{db['user']}:{db['password']}@localhost/{db['database']}", 
isolation_level='READ UNCOMMITTED')


Session = sessionmaker()


@contextmanager
def init_session():
    session = Session(bind = db_connection)
    session.expire_on_commit = False
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.expunge_all()
        session.close()

class DbValueNotFoundError(Exception):
    pass