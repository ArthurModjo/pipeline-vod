from methods import *
import socketio
import json

if __name__ == '__main__':

    sio = socketio.Client()
    @sio.event
    def connect():
        print('connection established')
        data =  {'data': 'foobar'}
        sio.emit('my_message', data)

    @sio.event
    def my_message(data):
        print('message received with ', data)
        sio.emit('my_message', {'response': 'my response'})

    @sio.event
    def identification(data):
        sio.emit('identification', {'response': 'langandsubtitles' })

    @sio.event
    def your_turn(data):
        """
        reçoit en parametre le nom du fichier compresse
        """
        #Detection de la langue
        print(data["response"])
        language, language_file = detect_language(data["response"])
        #Extraction des sous-titres
        subtilte_file = extract_subtitles(video_to_audio(data["response"]),language)
        data = {
            "language" : language_file,
            "subtitles" : subtilte_file,
            "video" : data["response"]
        }
        sio.emit('langandsubtitles_done', data)

    @sio.event
    def disconnect():
        print('disconnected from server')

    sio.connect('http://127.0.0.1:5000')
    sio.wait()
    # Attendez la déconnexion (ou utilisez une autre logique pour maintenir le programme en cours d'exécution)
    sio.wait()

   