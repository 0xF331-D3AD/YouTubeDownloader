import pytube
from pytube import YouTube

from combiner import combine_dto, combiner
from file_system import fs_utils
from mime_type import mime_type_enum
from youtube import youtube_dto


class YouTubeService:

    @staticmethod
    def __print_no_streams_match(all_streams: pytube.StreamQuery):
        print("\nSorry, can't proceed with download: no stream satisfies specified parameters."
              " Available streams are:\n")
        for s in all_streams:
            print(s)

    @staticmethod
    def __download_or_print_error(
            stream: pytube.StreamQuery or None,
            all_streams: pytube.StreamQuery,
            dto: youtube_dto.YouTubeDto,
            extension: str,
            type: str
    ) -> str or None:
        if stream is None:
            YouTubeService.__print_no_streams_match(all_streams)
            return None

        filename = dto.get_file_name() + f"-{type}" + '.' + extension
        stream.download(output_path=dto.get_output_directory(), filename=filename)
        return filename

    @staticmethod
    def __download_progressive(dto: youtube_dto.YouTubeDto):
        yt = YouTube(dto.get_url())
        file_extension = mime_type_enum.MimeType.MP4_VIDEO.value.get_extension_with_no_dot()
        resolution = None if dto.get_resolution() is None else dto.get_resolution().value
        all_streams = yt.streams
        stream = all_streams \
            .filter(progressive=True, file_extension=file_extension) \
            .filter(resolution=resolution) \
            .order_by('resolution') \
            .desc() \
            .first()

        YouTubeService.__download_or_print_error(stream, all_streams, dto, file_extension)

    @staticmethod
    def __download_not_progressive(dto: youtube_dto.YouTubeDto):
        yt = YouTube(dto.get_url())
        all_streams = yt.streams
        combined_dict = dict()
        for mt in dto.get_mime_types():
            combined = combined_dict.get(mt.get_subtype())
            if combined is None:
                combined_dict[mt.get_subtype()] = combine_dto.CombineDto(
                    dto.get_output_directory(), dto.get_file_name(), None, None, None
                )
            if mt.get_type() == 'audio':
                print(f"\n[+] Downloading {mt}")
                stream = all_streams.get_audio_only(mt.get_subtype())
                audio_path = YouTubeService.__download_or_print_error(stream, all_streams, dto,
                                                                      mt.get_extension_with_no_dot(), 'audio')
                if audio_path is not None:
                    combined_dict[mt.get_subtype()].set_audio_path(audio_path)
            elif mt.get_type() == 'video':
                print(f"\n[+] Downloading {mt}")
                stream = all_streams \
                    .filter(progressive=False, file_extension=mt.get_extension_with_no_dot()) \
                    .filter(resolution=dto.get_resolution().value) \
                    .order_by('resolution') \
                    .desc() \
                    .first()
                video_path = YouTubeService.__download_or_print_error(stream, all_streams, dto,
                                                                      mt.get_extension_with_no_dot(), 'video')
                if video_path is not None:
                    combined_dict[mt.get_subtype()].set_video_path(video_path)
                    combined_dict[mt.get_subtype()].set_extension(mt.get_extension_with_no_dot())

        for k, v in combined_dict.items():
            if v.can_be_combined():
                print(f"\n[+] Combining {k}")
                combiner.Combiner.combine_video_and_audio(v.get_video_path(), v.get_audio_path(), v.get_combined_path())
                fs_utils.delete_file(v.get_video_path())
                fs_utils.delete_file(v.get_audio_path())

    @staticmethod
    def download(dto: youtube_dto.YouTubeDto):
        if dto.get_progressive():
            YouTubeService.__download_progressive(dto)
        else:
            YouTubeService.__download_not_progressive(dto)
