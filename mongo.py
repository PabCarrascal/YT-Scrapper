import config
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
import globals


def connect():
    client = MongoClient(config.mongo_uri, server_api=ServerApi('1'))

    try:
        client.admin.command('ping')
        globals.set_global_mongo_client(client)
    except Exception as e:
        print("Unable to connect to MongoDB Atlas.")
        print(e)
    return client


def disconnect():
    globals.mongo_client.close()


def get_profile(channel_id):
    client = connect()
    database = client['yt-scrapper-db']
    collection = database['profiles']
    message_json = {"channel_id": channel_id}
    profile = collection.find_one(message_json)
    if profile is not None:
        return profile.get('essence')
    client.close()
    return profile


def persist_profile(channel_id, essence):
    client = connect()
    database = client['yt-scrapper-db']
    collection = database['profiles']
    profile_id = collection.insert_one({"channel_id": channel_id, "essence": essence})
    yt_profile = collection.find_one({"_id": profile_id})
    client.close()
    return yt_profile


def update_profile(channel_id, essence):
    client = connect()
    database = client['yt-scrapper-db']
    collection = database['profiles']
    message_filter = {"channel_id": channel_id}
    message_json = {"$set": {"essence": essence}}
    collection.update_one(message_filter, message_json)
    client.close()


def persist_message(channel_id, video_id, video_text):
    client = connect()
    database = client['yt-scrapper-db']
    collection = database['messages']
    message_json = {"channel_id": channel_id, "video_id": video_id, "video_text": video_text}
    collection.insert_one(message_json)
    client.close()


def get_message(channel_id, video_id):
    client = connect()
    database = client['yt-scrapper-db']
    collection = database['messages']
    message_json = {"channel_id": channel_id, "video_id": video_id}
    yt_video = collection.find_one(message_json)
    client.close()
    return yt_video


def get_all_messages(channel_id):
    client = connect()
    database = client['yt-scrapper-db']
    collection = database['messages']
    message_json = {"channel_id": channel_id}
    docs = collection.find(message_json)
    text_list = []
    for doc in docs:
        video_text = doc.get("video_text")
        if video_text:
            text_list.append(video_text)
    client.close()
    return text_list


def add_new_view(channel_id, video_id):
    client = connect()
    database = client['yt-scrapper-db']
    collection = database['views']
    message_json = {"channel_id": channel_id, "video_id": video_id, "createdDate": create_datetime(), "viewedDate": ""}
    collection.insert_one(message_json)
    client.close()


def update_view(channel_id, video_id):
    client = connect()
    database = client['yt-scrapper-db']
    collection = database['views']
    filter_row = {"channel_id": channel_id, "video_id": video_id}
    update = {"$set": {"viewedDate": create_datetime()}}
    result = collection.update_one(filter_row, update)
    if result.matched_count <= 0:
        print("No update was made for channel %s and video %s", channel_id, video_id)


def create_datetime():
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")
