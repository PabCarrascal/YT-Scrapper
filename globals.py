mongo_client = None


def set_global_mongo_client(mongo):
    global mongo_client
    mongo_client = mongo
