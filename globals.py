mongo_client = None
youtube_client = None


def set_global_youtube_client(youtube):
    global youtube_client
    youtube_client = youtube


def set_global_mongo_client(mongo):
    global mongo_client
    mongo_client = mongo
