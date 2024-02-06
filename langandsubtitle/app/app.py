from methods import *
import socketio

# Configure the source directory
working_directory = '/processing'

if __name__ == '__main__':

    sio = socketio.Client()
    @sio.event
    def connect():
        print('connection established')

    @sio.event
    def identification(data):
        sio.emit('identification',{'response': 'langandsubtitles' })

    @sio.event
    def test(data):
        print('test ', data)

    @sio.event
    def your_turn(data):
        """
        reçoit en parametre le nom du fichier compresse
        """
        #Detection de la langue
        print(data["response"])
        language, language_file = detect_language(working_directory+"/"+data["response"], working_directory)
        print("la langue est ",language, language_file)
        #Extraction des sous-titres
        subtilte_file = extract_subtitles(video_to_audio(working_directory+"/"+data["response"], working_directory),language, working_directory)

        data = {
            "langue" : language_file,
            "subtitles" : subtilte_file,
            "video" : data["response"]
        }
        sio.emit('langandsubtitles_done', data)

    @sio.event
    def disconnect():
        print('disconnected from server')

    sio.connect('http://172.20.0.10:5000')
    # Attendez la déconnexion (ou utilisez une autre logique pour maintenir le programme en cours d'exécution)
    sio.wait()

   