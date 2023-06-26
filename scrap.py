import googleapiclient.discovery
import config
import sys
import profile
import video


def main():
    youtube = googleapiclient.discovery.build(config.api_service_name, config.api_version,
                                              developerKey=config.developer_key)
    if len(sys.argv) != 3:
        print_help()
        exit(1)

    channel_id = sys.argv[2]

    if sys.argv[1] == "video":
        yt_video = video.get_random_video(youtube, channel_id)
    elif sys.argv[1] == "profile":
        yt_profile = profile.retrieve_profile(youtube, channel_id)
    else:
        print_help()
        exit(1)


def print_help():
    print("Usage: scrap <video|profile> <channelId>")
    print("Example: scrap video UCnws_li2Wmdc9peU0hQzS9A")


if __name__ == "__main__":
    main()
