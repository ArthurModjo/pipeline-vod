from moviepy.editor import VideoFileClip
import os
import socketio

working_directory = "/home/bad/LAB/pipeline-vod/processing"

def compress_video(input_path, output_directory, target_bitrate="250k"):
    try:
        # Charger la vidéo
        video_clip = VideoFileClip(input_path)

        # Définir le nom du fichier de sortie avec le suffixe "compressed"
        output_filename = f"{os.path.splitext(os.path.basename(input_path))[0]}_compressed.mp4"

        # Définir le chemin de sortie complet
        output_path = os.path.join(output_directory, output_filename)

        # Compresser la vidéo en ajustant le bitrate lors de l'écriture
        video_clip.write_videofile(output_path, codec="libx264", audio_codec="aac", bitrate=target_bitrate)

        print(f"La vidéo compressée a été enregistrée sous: {output_path}")

        # Supprimer les fichiers temporaires
        video_clip.close()
        audio_temp_path = os.path.splitext(output_path)[0] + ".aac"
        if os.path.exists(audio_temp_path):
            os.remove(audio_temp_path)
    
    except Exception as e:
        print(f"Une erreur s'est produite: {str(e)}")
    
    return output_filename

# Exemple d'utilisation
input_video_path = working_directory+"/demo2.mp4"
output_directory = "/home/bad/LAB/pipeline-vod/processing"


if __name__ == '__main__':
    sio = socketio.Client()
    @sio.event
    def connect():
        print('connection established')

    @sio.event
    def identification(data):
        sio.emit('identification',{'response': 'downscale' })

    @sio.event
    def your_turn(data):
        compressed_video = compress_video(working_directory+'/'+data["response"], working_directory)
        sio.emit('compression_done', {'response': compressed_video})

    @sio.event
    def disconnect():
        print('disconnected from server')

    sio.connect('http://localhost:5000')



