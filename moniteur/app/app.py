import eventlet
import socketio


sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})

#Dictionnaire des client connectés avec leur services et leur id
clients = {}

@sio.event
def connect(sid, environ):
    sio.emit('identification',{'response': 'ask_for_identification'})
    print('connect ', sid)

@sio.event
def my_message(sid, data):
    print('message ', data['data'])

@sio.event
def identification(sid, data):
    print('identification ', data)
    clients[data["response"]] = sid

@sio.event
def compression_done(sid, data):
    sio.emit('your_turn',{'response': data}, room=clients["langandsubtitles"])

@sio.event
def langandsubtitles_done(sid, data):
    print('langandsubtitles_done ', data)
    sio.emit('your_turn',{'response': data['video']}, room=clients["animaldetector"])

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)