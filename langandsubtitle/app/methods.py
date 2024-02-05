import langdetect
from moviepy.video.io.VideoFileClip import VideoFileClip
import os
import wave
import sys
from vosk import Model, KaldiRecognizer
import moviepy.editor as mp
import speech_recognition as sr
from langdetect import detect
import json

#DETECTION DE LA LANGUE 
def detect_language(video_path, output_folder):
    # Charger la vidéo et extraire les 10 premières secondes de l'audio
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    video_clip = VideoFileClip(video_path)
    audio_clip = video_clip.audio.subclip(0,5)
    audio_clip.write_audiofile(os.path.join(output_folder, "temp_audio.wav"), codec='pcm_s16le', ffmpeg_params=["-ac", "1", "-ar", "16000"])

    # Utiliser langdetect pour détecter la langue
    try:
        with open(os.path.join(output_folder, "temp_audio.wav"), "rb") as file:
            audio_text = file.read().decode("utf-8", errors="ignore")

        detected_language = langdetect.detect(audio_text)
        with open(os.path.join(output_folder, video_name+"_lang.txt"), 'w') as f:
            f.write(detected_language)
        return detected_language, os.path.join(output_folder, video_name+"_lang.txt")
    except langdetect.lang_detect_exception.LangDetectException as e:
        return f"Erreur lors de la détection de la langue : {e}"
    finally:
        # Supprimer le fichier temporaire à la fin
        if os.path.exists(os.path.join(output_folder, "temp_audio.wav")):
            os.remove(os.path.join(output_folder, "temp_audio.wav"))

#VIDEO TO AUDIO
def video_to_audio(video_path, output_folder):
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    video_clip = mp.VideoFileClip(video_path)
    audio = video_clip.audio

    if audio is None:
        print("Aucune piste audio disponible dans la vidéo.")
        return

    audio.write_audiofile(os.path.join(output_folder, f"{video_name}.wav"), codec="pcm_s16le", ffmpeg_params=["-ac", "1", "-ar", "16000"])
    return os.path.join(output_folder, f"{video_name}.wav")


#EXTRACTION DES SOUS TITRES
def extract_subtitles(audio_path, language, output_folder):
    nom_audio = os.path.splitext(os.path.basename(audio_path))[0]
    wf = wave.open(audio_path, "rb")
    
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print("Audio file must be WAV format mono PCM.")
        sys.exit(1)

    model = Model(lang=language)
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(False)
    rec.SetPartialWords(True)

    while True:
        data = wf.readframes(3000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            pass
        else:
            pass

    wf.close()
    if os.path.exists(audio_path):
        os.remove(audio_path)
    
    final_result = json.loads(rec.FinalResult())
    # Rediriger la sortie vers un fichier
    with open(os.path.join(output_folder, nom_audio+"_subtitles.txt"), 'w') as f:
        f.write(final_result['text'])
        os.path.join(output_folder, nom_audio+"_subtitles.txt")
    return nom_audio+"_subtitles.txt"

if __name__ == '__main__':
    print(detect_language("/home/bad/LAB/pipeline-vod/processing/demo2.mp4", "./"))
    print(extract_subtitles("/home/bad/LAB/pipeline-vod/langandsubtitle/app/demo2.wav", "en-us", "./"))