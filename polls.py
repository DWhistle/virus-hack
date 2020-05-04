import eventlet
import socketio
from private.config import Configurator
Configurator.configure_resources()
from private.db.models.education import DbMethods
import json

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)



@sio.on('insertpoll')
def insert_poll(uid, data):
    print(data)
    poll = json.loads(data)
    print('insertpoll ', poll)



@sio.on('publishpoll')
def publish_poll(uid, data):
    sio.emit('publish', data)

@sio.event
def connect(sid, environ):
    print('connected ', sid)

@sio.event
def disconnect(sid):
    print('disconnected ', sid)

eventlet.wsgi.server(eventlet.listen(('', 5555)), app)