import os


class CombineDto:
    def __init__(self, output_directory: str, filename: str, extension: str or None, video_path: str or None,
                 audio_path: str or None):
        self.__output_directory = output_directory
        self.__extension = extension
        self.__filename = filename
        self.__video_path = video_path
        self.__audio_path = audio_path

    def get_video_path(self):
        return self.__video_path

    def set_video_path(self, video_path):
        self.__video_path = os.path.join(self.__output_directory, video_path)

    def get_audio_path(self):
        return self.__audio_path

    def set_audio_path(self, audio_path):
        self.__audio_path = os.path.join(self.__output_directory, audio_path)

    def set_extension(self, extension):
        self.__extension = extension

    def can_be_combined(self):
        return (self.__video_path is not None) and (self.__audio_path is not None)

    def get_combined_path(self):
        combined_filename = self.__filename + '-combined.' + self.__extension
        return os.path.join(self.__output_directory, combined_filename)

    def __repr__(self):
        return f"combined_path = {self.get_combined_path()}, can be combined = {self.can_be_combined()}, " \
               f"vp = {self.__video_path}, ap = {self.__audio_path}"
