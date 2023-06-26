import config
from youtube import get_playlists_from_channel
from youtube import get_playlist_item_info
from transcribe_audio import transcribe_video
from mongo import get_profile
from mongo import update_profile
from mongo import persist_profile
from mongo import get_message
from mongo import get_all_messages
from mongo import persist_message


def retrieve_profile(youtube_client, channel_id):
    yt_profile = check_profile(channel_id)
    video_texts = get_all_messages(channel_id)
    playlist_from_channel = get_playlists_from_channel(youtube_client, channel_id)['items']
    new_videos = False
    for playlist in playlist_from_channel:
        items = get_playlist_item_info(youtube_client, playlist['id'])
        for item in items["items"]:
            video_id = item["contentDetails"]["videoId"]
            yt_video = get_message(channel_id, video_id)
            if yt_video is None:
                new_videos = True
                url = config.yt_watch + video_id
                video_text = transcribe_video(url)
                persist_message(channel_id, video_id, video_text)
                video_texts.append(video_text + ".\n")
            else:
                video_texts.append(yt_video + ".\n")

    if new_videos:
        essence = config.profile_message.replace("<texts>", video_texts)
        update_profile(channel_id, essence)
        yt_profile = check_profile(channel_id)

    return {"profile": yt_profile}


def check_profile(channel_id):
    yt_profile = get_profile(channel_id)
    if yt_profile is None:
        return persist_profile(channel_id, config.profile_message)
