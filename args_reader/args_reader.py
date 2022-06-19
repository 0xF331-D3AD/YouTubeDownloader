import argparse

from pytube import YouTube

from file_system import fs_utils
from mime_type import mime_type_enum
from youtube import youtube_dto, resolutions_enum


class ArgsReader:
    def __init__(self):
        self.__default_mime_types = [
            mime_type_enum.MimeType.MP4_VIDEO.value,
            mime_type_enum.MimeType.MP4_AUDIO.value,
        ]
        self.__default_resolution = None

    @staticmethod
    def __fix_output_dir(output_directory: str or None) -> str:
        if output_directory is None or output_directory == '':
            return fs_utils.get_downloads_path()
        abs_path = fs_utils.get_abs_path(output_directory)
        fs_utils.make_dirs_recursively(abs_path)
        return abs_path

    @staticmethod
    def __fix_file_name(filename: str or None, yt: YouTube) -> str:
        if filename is None or filename == '':
            return yt.title

        only_name = fs_utils.get_file_name_without_directory(filename)
        if only_name is None or only_name == '':
            only_name = yt.title
        return only_name

    @staticmethod
    def __compute_is_progressive(mime_types: list,
                                 resolution: resolutions_enum.Resolution or None) -> bool:
        return len(mime_types) == 0 and resolution is None

    @staticmethod
    def __verify_mime_types(mime_types: list):
        available_types = mime_type_enum.MimeType.get_available_mime_types()
        for http_repr in mime_types:
            if http_repr not in available_types:
                raise ValueError(f"No such mime type: {http_repr}")

    @staticmethod
    def __verify_combine_audio_with_video(combine_audio_with_video: bool, real_mime_types: list):
        if not combine_audio_with_video:
            return
        as_set = set(real_mime_types)
        subtype_dict = dict()
        if len(as_set) > 1:
            for mt in as_set:
                subtype = mt.get_subtype()
                existing = subtype_dict.get(subtype)
                if existing is None:
                    subtype_dict[subtype] = 0
                subtype_dict[subtype] += 1

            amount_of_subtypes_without_pair = 0
            for k, v in subtype_dict.items():
                if v <= 1:
                    amount_of_subtypes_without_pair += 1
            if amount_of_subtypes_without_pair == len(subtype_dict):
                raise ValueError("Invalid configuration: cannot merge files with different extensions")

    def __compute_mime_types(self, selected_mime_types: list) -> list:
        if len(selected_mime_types) == 0:
            return self.__default_mime_types
        else:
            return mime_type_enum.MimeType.map_http_representations_to_dtos(selected_mime_types)

    def read_args(self) -> youtube_dto.YouTubeDto:
        description = "Program allows you to download videos and audios from YouTube, even if " \
                      "no 'download' link is provided. The default quality will be 720p or lower. If you" \
                      " want to increase the quality, use --resolution flag. By default, audio and video will not" \
                      " be combined. Use -c flag to get a video with audio. Audio with no video and video with no" \
                      " audio will be removed"
        all_args = argparse.ArgumentParser(description=description)

        all_args.add_argument("-u", "--url", required=True,
                              help="YouTube url of the video")
        all_args.add_argument("-od", "--output-directory", required=False,
                              help="The directory where the video will be saved")
        all_args.add_argument("-of", "--output-filename", required=False,
                              help="The name of file where the vide will be saved")
        all_args.add_argument("--mime-types", required=False, default=[], nargs='*',
                              help=f"If not specified, the \"progressive download\" will be chosen ("
                                   f"The legacy stream that contain the audio and video in a single file,"
                                   f" quality will be less or equal to 720p)"
                                   f" with mime types audio|video/mp4. Available mime types are:"
                                   f" {mime_type_enum.MimeType.get_available_mime_types()}."
                              )
        all_args.add_argument("-c", "--combine-audio-with-video", required=False, default=False, type=bool,
                              help="If progressive download is not chosen, then you'll end up with separate"
                                   " video and audio file. This option combines video and audio into 1 file"
                                   " if their extensions match. Audio with no video and video with no"
                                   " audio will be removed"
                              )
        all_args.add_argument("-r", "--resolution", required=False, default=self.__default_resolution,
                              help=f"Specify the resolution of the video. Available"
                                   f" resolutions are: {resolutions_enum.Resolution.get_available_resolutions()}"
                              )

        args = vars(all_args.parse_args())
        self.__verify_mime_types(args.get('mime_types'))
        args['output_directory'] = self.__fix_output_dir(args.get('output_directory'))
        yt = YouTube(args.get('url'))
        args['output_filename'] = self.__fix_file_name(args.get('output_filename'), yt)

        resolution = resolutions_enum.Resolution.from_name(args.get('resolution'))
        mime_types = self.__compute_mime_types(args.get('mime_types'))
        self.__verify_combine_audio_with_video(args.get('combine_audio_with_video'), mime_types)

        return youtube_dto.YouTubeDto(
            args.get('url'),
            args.get('output_directory'),
            args.get('output_filename'),
            self.__compute_is_progressive(args.get('mime_types'), resolution),
            mime_types,
            resolution,
            args.get('combine_audio_with_video')
        )
