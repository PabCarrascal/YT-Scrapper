from pytube import YouTube
import whisper
import os

file_name = "yt_video_sound.mp4"


def transcribe_video(video_url):
    global yt
    try:
        try:
            yt = YouTube(video_url)
        except Exception as io:
            print("Connection error. \n%s", io)

        yt.streams.filter(file_extension="mp4")
        stream = yt.streams.get_by_itag(139)
        stream.download('', file_name)
        model = whisper.load_model("base")
        result = model.transcribe(file_name)
        delete_file()
        return result["text"]
    except Exception as e:
        print("Error transcribing a video. \n%s", e)
        delete_file()


def delete_file():
    if os.path.exists(file_name):
        os.remove(file_name)
