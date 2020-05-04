import eventlet
import socketio

sio = socketio.Server()
app = socketio.WSGIApp(sio)

@sio.on('sendpoll')
def insert_poll(data):
    print('sendpoll ', data)


@sio.on('getpoll')
def get_poll(data):
    print(data)
    sio.emit('response')

@sio.on('disconnect')
def disconnected():
    print('disconnected')
@sio.on('connect')
def connected():
    print('connected')

eventlet.wsgi.server(eventlet.listen(('', 5555)), app)