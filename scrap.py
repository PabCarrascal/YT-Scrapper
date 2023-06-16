# -*- coding: utf-8 -*-
import random
import time
import subprocess
import googleapiclient.discovery
import json
import config
import sys


def main():
    global youtube
    youtube = googleapiclient.discovery.build(config.api_service_name, config.api_version,
                                              developerKey=config.developer_key)
    if len(sys.argv) != 3:
        print_help()
        exit(1)

    if sys.argv[1] == "video":
        get_random_video()
    elif sys.argv[1] == "profile":
        get_profile()
    else:
        print_help()
        exit(1)


def get_random_video():
    playlist_from_channel = get_playlists_from_channel(config.channel_id)['items']
    random_playlist = get_info(random.choice(playlist_from_channel))
    random_playlist_item = get_playlist_item_info(random_playlist['id'])
    video_id = random.choice(random_playlist_item['items'])['contentDetails']['videoId']
    open_new_container(config.yt_watch + video_id, get_video_seconds(get_video_info(video_id)))
    return


def get_profile():
    playlists = []
    playlist_from_channel = get_playlists_from_channel(config.channel_id)['items']
    for pl in playlist_from_channel:
        item = get_playlist_item_info(get_info(pl)['id'])
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
    video_duration = get_info(video['items'][0]['contentDetails']['duration'])[2:]
    position_m = video_duration.find("M")
    seconds = (int(video_duration[:position_m]) * 60) + int(video_duration[position_m + 1:-1])
    return seconds - 60 if seconds >= 180 else seconds


def get_info(info):
    return json.loads(json.dumps(info))


def get_playlists_from_channel(channel_id):
    request = youtube.playlists().list(
        part="contentDetails",
        channelId=channel_id
    )
    return get_info(request.execute())


def get_playlist_info(playlist_id):
    request = youtube.playlists().list(
        part="contentDetails,id,localizations,player,snippet,status",
        id=playlist_id
    )

    return get_info(request.execute())


def get_playlist_item_info(item_id):
    request = youtube.playlistItems().list(
        part="contentDetails",
        playlistId=item_id
    )
    return get_info(request.execute())


def get_video_info(video_id):
    request = youtube.videos().list(
        part="contentDetails",
        id=video_id
    )
    return get_info(request.execute())


def print_help():
    print("Usage: scrap <video|profile> <channelId>")
    print("Example: scrap video UCnws_li2Wmdc9peU0hQzS9A")


if __name__ == "__main__":
    global youtube
    main()
