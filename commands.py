from sqlalchemy import MetaData
from flask.cli import FlaskGroup
from main import app
from private.db.models import db_connection


meta = MetaData()
meta.bind = db_connection
client = FlaskGroup(app)
@client.command("drop_db")
def drop_all():
    meta.drop_all()



if __name__ == "__main__":
    client()