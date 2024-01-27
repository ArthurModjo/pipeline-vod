from flask import Flask
import os, ffmpeg
app = Flask(__name__)

@app.route('/')
def hello():
	return os.getcwd()

@app.route('/downscale/<path:filename>')
def downscale(filename):
    # Get the file
    file = os.path.join(os.getcwd(), filename)
    # Get the file extension
    ext = os.path.splitext(file)[1]
    # Check if the file is a video
    if ext == '.mp4':
        # Construire le chemin de sortie pour le fichier downscalé dans le répertoire 'output'
        output_directory = os.path.join(os.getcwd(), 'output')
        # Vérifier si le répertoire de sortie existe, sinon le créer
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        # Create the output file name
        output = os.path.join(os.getcwd(), 'output', os.path.basename(file))
        # Downscale the video
        try:
            ffmpeg.input(file).output(output, s='hd480', acodec='copy', vcodec='libx264', crf=23, preset='veryfast').run()
        except ffmpeg.Error as e:
            print('Erreur ffmpeg :', e.stderr)
        # Return the output file
        return output
    else:
        # Return the original file
        return file

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)