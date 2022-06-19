from args_reader import args_reader
from youtube import youtube_service


def main():
    youtube_dto = args_reader.ArgsReader().read_args()
    print(youtube_dto)
    youtube_service.YouTubeService.download(youtube_dto)


if __name__ == '__main__':
    main()
