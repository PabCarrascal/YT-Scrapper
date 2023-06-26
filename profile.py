import json
import youtube
import config


def get_profile(youtube_client):
    playlists = []
    playlist_from_channel = youtube_client.get_playlists_from_channel(youtube_client, config.channel_id)['items']
    for pl in playlist_from_channel:
        item = youtube_client.get_playlist_item_info(youtube_client.get_info(pl)['id'])
    return

