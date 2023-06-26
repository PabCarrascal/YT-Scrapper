import json


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


def get_playlist_item_info(youtube, item_id):
    request = youtube.playlistItems().list(
        part="contentDetails",
        playlistId=item_id
    )
    return get_info(request.execute())


def get_video_info(youtube, video_id):
    request = youtube.videos().list(
        part="contentDetails",
        id=video_id
    )
    return get_info(request.execute())

