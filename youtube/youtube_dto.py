from youtube import resolutions_enum


class YouTubeDto:
    def __init__(self, url: str,
                 output_directory: str,
                 filename: str,
                 progressive: bool,
                 mime_types: list,
                 resolution: resolutions_enum.Resolution,
                 combine_audio_with_video: bool,
                 ):
        self.__url = url
        self.__output_directory = output_directory
        self.__filename = filename
        self.__progressive = progressive
        self.__mime_types = mime_types
        self.__resolution = resolution
        self.__combine_audio_with_video = combine_audio_with_video

    def get_url(self):
        return self.__url

    def get_output_directory(self):
        return self.__output_directory

    def get_file_name(self):
        return self.__filename

    def get_progressive(self):
        return self.__progressive

    def get_mime_types(self):
        return self.__mime_types

    def get_resolution(self) -> resolutions_enum.Resolution:
        return self.__resolution

    def get_combine_audio_with_video(self):
        return self.__combine_audio_with_video

    def __str__(self):
        url = "[+] Downloading from {}".format(self.get_url())
        output_dir = "[+] Will be saved to {}".format(self.get_output_directory())
        file_name = "[+] File name will be {}".format(self.get_file_name())
        progressive = '[+] Is download progressive: {}'.format(self.get_progressive())
        mime_types = '[+] Selected mime types: {}'.format(self.get_mime_types())
        combine_audio_with_video = '[+] Combine audio with video: {}'.format(self.get_combine_audio_with_video())
        resolution = '[+] Resolution is {} ({})'.format(
            self.get_resolution().name, self.__resolution.value
        ) if self.get_resolution() is not None else '[+] Resolution will be the highest available'
        newline = '\n'
        return f"{url}{newline}{output_dir}{newline}{file_name}{newline}{progressive}{newline}{mime_types}" \
               f"{newline}{combine_audio_with_video}{newline}{resolution}"

    def __repr__(self):
        return self.__str__()
