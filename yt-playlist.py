# -*- coding: utf-8 -*-
import googleapiclient.discovery

def main():
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyDuJxMUPp4KmvVWpIjRaQte12qQzrB9gUs"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    request = youtube.playlists().list(
        part="snippet",
        channelId="UCnws_li2Wmdc9peU0hQzS9A",
        maxResults=25
    )
    response = request.execute()

    print(response)

if __name__ == "__main__":
    main()