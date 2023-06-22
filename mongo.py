import config
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


def connect():
    # Create a new client and connect to the server
    client = MongoClient(config.mongo_uri, server_api=ServerApi('1'))

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
    except Exception as e:
        print("Unable to connect to MongoDB Atlas.")
        print(e)
    return client


def persist_profile(channel_id, essence):
    client = connect()
    database = client['yt-scrapper-db']
    collection = database['profiles']
    message_json = {"channel_id": channel_id, "essence": essence}
    collection.insert_one(message_json)
    client.close()


def get_profile(channel_id):
    client = connect()
    database = client['yt-scrapper-db']
    collection = database['profiles']
    message_json = {"channel_id": channel_id}
    profile = collection.find_one(message_json).get('essence')
    client.close()
    return profile


def persist_message(channel_id, video_id, video_text):
    client = connect()
    database = client['yt-scrapper-db']
    collection = database['messages']
    message_json = {"channel_id": channel_id, "video_id": video_id, "video_text": "{\"role\": \"user\", \"content\": " + video_text + "}"}
    collection.insert_one(message_json)
    client.close()


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
