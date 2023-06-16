import config
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


def connect():
    # Create a new client and connect to the server
    client = MongoClient(config.mongo_uri, server_api=ServerApi('1'))

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("You successfully connected to MongoDB!")

    except Exception as e:
        print("Unable to connect to MongoDB Atlas.")
        print(e)
    return client


def persist():
    client = connect()
    bbdd = client['yt-scrapper-db']
    collection = bbdd['messages']
    return


def get_all():
    connect()
    return


if __name__ == "__main__":
    connect()
