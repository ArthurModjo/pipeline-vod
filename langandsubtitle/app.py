from methods import *

if __name__ == '__main__':
    video_path = "./demo2.mp4"

    #Language detection
    langue = detect_language(video_path)
    #Extraction des sous-titres
    extract_subtitles(video_to_audio(video_path),langue)
   