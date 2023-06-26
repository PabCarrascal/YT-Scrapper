import json
import config
from youtube import get_playlists_from_channel
from youtube import get_playlist_item_info
from youtube import get_info


def get_profile(youtube_client):
    playlists = []
    playlist_from_channel = get_playlists_from_channel(youtube_client, config.channel_id)['items']
    for pl in playlist_from_channel:
        item = get_playlist_item_info(youtube_client, get_info(pl)['id'])
    return

