from pytube import YouTube
import whisper
import os

file_name = "yt_video_sound.mp4"


def transcribe_video(video_url):
    global yt
    try:
        try:
            yt = YouTube(video_url)
        except:
            print("Connection error")

        yt.streams.filter(file_extension="mp4")
        stream = yt.streams.get_by_itag(139)
        stream.download('', file_name)
        model = whisper.load_model("base")
        result = model.transcribe(file_name)
        deleteFile()
        return result["text"]
    except:
        deleteFile()


def deleteFile():
    if os.path.exists(file_name):
        os.remove(file_name)
