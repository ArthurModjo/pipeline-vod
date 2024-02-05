# Description: Serveur de communication entre les services et le moniteur   
import eventlet
import socketio
import os
from flask import Flask, render_template, request
import json

sio = socketio.Server(cors_allowed_origins="*")
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "/home/bad/LAB/pipeline-vod/processing"


# Dictionnaire des client connectés avec leur services et leur id
clients = {}
progressing  = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/to-process', methods=['POST'])
def to_process():
    # Save the file
    if 'file' not in request.files:
        return 'Aucun fichier sélectionné'

    file = request.files['file']
    if file.filename == '':
        return 'Nom de fichier vide'

    if file and file.filename.split('.')[-1] in ['mp4', 'avi', 'mov']:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], (file.filename).replace(' ', '_')))
        sio.emit('your_turn', {'response': (file.filename).replace(' ', '_')}, room=clients["downscale"])
        return 'Fichier téléchargé avec succès'
    else:
        return 'Extension de fichier non autorisée'

@app.route('/processing', methods=['GET'])
def processing():
    return render_template('processing.html')

@app.route('/progress', methods=['GET'])
def progress():
    response_data ='{"progressing": "'+str(progressing)+'"}'
    return json.loads(response_data)

@sio.event
def connect(sid, environ):
    sio.emit('identification', {'response': 'ask_for_identification'})
    print('connect ', sid)


@sio.event
def identification(sid, data):
    clients[data["response"]] = sid
    print(clients)

@sio.event
def compression_done(sid, data):
    #update the progressing value
    global progressing
    progressing = 1
    sio.emit('your_turn',{'response': data['response']}, room=clients["langandsubtitles"])

@sio.event
def langandsubtitles_done(sid, data):
    #update the progressing value
    global progressing
    progressing = 3
    print('langandsubtitles_done ', data)
    print(data)
    sio.emit('your_turn',{'response': data['video']}, room=clients["animaldetector"])

@sio.event
def animaldetector_done(sid, data):
    #update the progressing value
    global progressing
    progressing = 4
    print('animaldetector_done ', data)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

# Other events and routes go here...

if __name__ == '__main__':
    # Wrap the Socket.IO application with the Flask applicationx
    app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)
    eventlet.wsgi.server(eventlet.listen(('127.0.0.1', 5000)), app)
