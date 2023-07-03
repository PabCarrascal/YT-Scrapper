import googleapiclient.discovery
import json
import globals
import config


def connect():
    youtube = None
    try:
        youtube = googleapiclient.discovery.build(config.api_service_name, config.api_version,
                                                  developerKey=config.yt_developer_key)
    except Exception as e:
        print("Unable to connect to to Youtube API")
        print(e)

    globals.set_global_youtube_client(youtube)


def get_playlists_from_channel(youtube, channel_id):
    request = youtube.playlists().list(
        part="contentDetails",
        channelId=channel_id
    )
    return get_info(request.execute())


def get_info(info):
    return json.loads(json.dumps(info))


def get_playlist_info(youtube, playlist_id):
    request = youtube.playlists().list(
        part="contentDetails,id,localizations,player,snippet,status",
        id=playlist_id
    )

    return get_info(request.execute())


def get_items_from_playlist(youtube, playlist_id, token=None):
    request = youtube.playlistItems().list(
        part="contentDetails",
        pageToken=token,
        playlistId=playlist_id
    )
    return get_info(request.execute())


def get_video_info(youtube, video_id):
    request = youtube.videos().list(
        part="contentDetails",
        id=video_id
    )
    return get_info(request.execute())
