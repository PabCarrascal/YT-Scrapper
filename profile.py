import config
import youtube
import transcribe_audio
import mongo
import globals


def retrieve_profile(channel_id):
    youtube.connect()
    mongo.connect()

    yt_profile = check_profile(channel_id)
    video_texts = mongo.get_all_messages(channel_id)
    playlist_from_channel = youtube.get_playlists_from_channel(globals.youtube_client, channel_id)['items']
    new_videos = False
    # for playlist in playlist_from_channel:
    playlist = playlist_from_channel[0]
    items = check_playlist_items(globals.youtube_client, playlist['id'])
    for item in items:
        video_id = item["contentDetails"]["videoId"]
        yt_video = mongo.get_message(channel_id, video_id)
        if yt_video is None:
            new_videos = True
            url = config.yt_watch + video_id
            video_text = transcribe_audio.transcribe_video(url)
            mongo.persist_message(channel_id, video_id, video_text)
            video_texts.append(video_text + ".\n")
        else:
            video_texts.append(yt_video['video_text'] + ".\n")

    if new_videos:
        essence = config.profile_message.replace("<texts>", " ".join(video_texts))
        mongo.update_profile(channel_id, essence)
        yt_profile = check_profile(channel_id)

    mongo.disconnect()
    return {"profile": yt_profile}


def check_playlist_items(youtube_client, playlist_id):
    all_items = []
    response = youtube.get_items_from_playlist(youtube_client, playlist_id)
    for item in response['items']:
        all_items.append(item)
    while 'nextPageToken' in response:
        token = response['nextPageToken']
        response = youtube.get_items_from_playlist(youtube_client, playlist_id, token)
        for item in response['items']:
            all_items.append(item)
    return all_items


def check_profile(channel_id):
    yt_profile = mongo.get_profile(channel_id)
    if yt_profile is None:
        return mongo.persist_profile(channel_id, config.profile_message)
    return yt_profile
