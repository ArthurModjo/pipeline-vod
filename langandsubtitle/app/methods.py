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
def detect_language(video_path):
    # Charger la vidéo et extraire les 10 premières secondes de l'audio
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    video_clip = VideoFileClip(video_path)
    audio_clip = video_clip.audio.subclip(0,5)
    audio_clip.write_audiofile("temp_audio.wav", codec='pcm_s16le', ffmpeg_params=["-ac", "1", "-ar", "16000"])

    # Utiliser langdetect pour détecter la langue
    try:
        with open("temp_audio.wav", "rb") as file:
            audio_text = file.read().decode("utf-8", errors="ignore")

        detected_language = langdetect.detect(audio_text)
        #print("la lanque est : ",detected_language)
        with open(video_name+"_lang.txt", 'w') as f:
            f.write(detected_language)
        return detected_language,video_name+"_lang.txt"
    except langdetect.lang_detect_exception.LangDetectException as e:
        return f"Erreur lors de la détection de la langue : {e}"
    finally:
        # Supprimer le fichier temporaire à la fin
        if os.path.exists("temp_audio.wav"):
            os.remove("temp_audio.wav")

#VIDEO TO AUDIO
def video_to_audio(video_path):
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    video_clip = mp.VideoFileClip(video_path)
    audio = video_clip.audio

    if audio is None:
        print("Aucune piste audio disponible dans la vidéo.")
        return

    audio.write_audiofile(f"{video_name}.wav", codec="pcm_s16le", ffmpeg_params=["-ac", "1", "-ar", "16000"])
    return f"{video_name}.wav"


#EXTRACTION DES SOUS TITRES
def extract_subtitles(audio_path, language):
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
            # print(rec.Result())
        else:
            # print(rec.PartialResult())
            pass

    wf.close()
    if os.path.exists(audio_path):
        os.remove(audio_path)
    
    final_result = json.loads(rec.FinalResult())
    # Rediriger la sortie vers un fichier
    with open(nom_audio+"_subtitles.txt", 'w') as f:
        f.write(final_result['text'])
    return nom_audio+"_subtitles.txt"

