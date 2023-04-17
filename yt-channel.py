# -*- coding: utf-8 -*-

import googleapiclient.discovery

def main():

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyDuJxMUPp4KmvVWpIjRaQte12qQzrB9gUs"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    request = youtube.channels().list(
        part="contentDetails,id,snippet,statistics,status,topicDetails",
        id="UCnws_li2Wmdc9peU0hQzS9A"
    )
    response = request.execute()

    print(response)

if __name__ == "__main__":
    main()