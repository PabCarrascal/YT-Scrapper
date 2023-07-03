import sys
import profile
import video


def main():
    if len(sys.argv) != 3:
        print_help()
        exit(1)

    channel_id = sys.argv[2]

    if sys.argv[1] == "video":
        video.get_random_video(channel_id)
    elif sys.argv[1] == "profile":
        profile.retrieve_profile(channel_id)
    else:
        print_help()
        exit(1)


def print_help():
    print("Usage: scrap <video|profile> <channelId>")
    print("Example: scrap video UCnws_li2Wmdc9peU0hQzS9A")


if __name__ == "__main__":
    main()
