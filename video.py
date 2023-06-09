import config
import random
from youtube import get_playlists_from_channel
from youtube import get_items_from_playlist
from youtube import get_info
from youtube import get_video_info
import subprocess
import time
import globals


def get_random_video(channel_id):
    playlist_from_channel = get_playlists_from_channel(globals.youtube_client, channel_id)['items']
    random_playlist = get_info(random.choice(playlist_from_channel))
    random_playlist_item = get_items_from_playlist(globals.youtube_client, random_playlist['id'])
    video_id = random.choice(random_playlist_item['items'])['contentDetails']['videoId']
    open_new_container(config.yt_watch_url + video_id, get_video_seconds(get_video_info(globals.youtube_client, video_id)))
    return


def open_new_container(video_link, seconds):
    try:
        subprocess.run(["docker", "run", "--name", "yt-linux", "-e", "LINK=" + video_link, "-d", "mongo"])
        while seconds > 0:
            time.sleep(1)
            seconds -= 1
        subprocess.run(["docker", "stop", "yt-linux"])
    except Exception as e:
        print(e)
        print("Check if docker is running.")


def get_video_seconds(video):
    video_duration = get_info(video['items'][0]['contentDetails']['duration'])[2:]
    position_m = video_duration.find("M")
    seconds = (int(video_duration[:position_m]) * 60) + int(video_duration[position_m + 1:-1])
    return seconds - 60 if seconds >= 180 else seconds
