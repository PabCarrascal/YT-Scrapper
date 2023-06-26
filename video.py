import config
import random
import youtube
import subprocess
import time


def get_random_video(youtube_client):
    playlist_from_channel = youtube_client.get_playlists_from_channel(youtube_client, config.channel_id)['items']
    random_playlist = youtube.get_info(random.choice(playlist_from_channel))
    random_playlist_item = youtube.get_playlist_item_info(youtube_client, random_playlist['id'])
    video_id = random.choice(random_playlist_item['items'])['contentDetails']['videoId']
    open_new_container(config.yt_watch + video_id, get_video_seconds(youtube.get_video_info(youtube, video_id)))
    return


def open_new_container(video_link, seconds):
    try:
        subprocess.run(["docker", "run", "--name", "yt-linux", "-e", "LINK=" + video_link, "-d", "mongo"])
        while seconds > 0:
            time.sleep(1)
            seconds -= 1
        subprocess.run(["docker", "stop", "yt-linux"])
    except Exception:
        print("Check if docker is running.")


def get_video_seconds(video):
    video_duration = youtube.get_info(video['items'][0]['contentDetails']['duration'])[2:]
    position_m = video_duration.find("M")
    seconds = (int(video_duration[:position_m]) * 60) + int(video_duration[position_m + 1:-1])
    return seconds - 60 if seconds >= 180 else seconds
