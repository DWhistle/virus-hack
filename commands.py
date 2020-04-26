from sqlalchemy import MetaData
from flask.cli import FlaskGroup
from main import app
from private.db.models import db_connection
from private.db.models.identity import meta
from private.db.models.education import *


meta.bind = db_connection
client = FlaskGroup(app)
@client.command("drop_db")
def drop_all():
    meta.drop_all()

@client.command("create_db")
def create_all():
    meta.create_all()



if __name__ == "__main__":
    client()