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
    poll = json.dumps({"id": 1,
                "teacher_id": 14,
                "student": 15,
                "question": "Что ищут в темной комнате?",
                "answers": "Кошку;Собаку;!!Черную кошку!!;Лошадь",
                "mark": 0,})
    sio.emit('publish', poll)

@sio.event
def connect(sid, environ):
    print('connected ', sid)

@sio.event
def disconnect(sid):
    print('disconnected ', sid)

eventlet.wsgi.server(eventlet.listen(('', 5555)), app)