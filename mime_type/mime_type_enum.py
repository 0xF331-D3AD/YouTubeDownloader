from enum import Enum
from functools import cmp_to_key

from mime_type import mime_type_dto


class MimeType(Enum):
    MP4_AUDIO = mime_type_dto.MimeTypeDto('audio/mp4', 'mp3')
    MP4_VIDEO = mime_type_dto.MimeTypeDto('video/mp4', 'mp4')
    WEBM_AUDIO = mime_type_dto.MimeTypeDto('audio/webm', 'webm')
    WEBM_VIDEO = mime_type_dto.MimeTypeDto('video/webm', 'webm')

    @staticmethod
    def __mime_type_http_repr_comparator(http_repr_1: str, http_repr_2: str) -> int:
        parts1 = http_repr_1.split('/')
        parts2 = http_repr_2.split('/')
        if parts1[1] == parts2[1]:
            return int(parts1[0] < parts2[0])
        return int(parts1[1] < parts2[1])

    @staticmethod
    def get_available_mime_types() -> list:
        out = list()
        for e in list(MimeType):
            out.append(e.value.get_http_representation())
        out.sort(key=cmp_to_key(MimeType.__mime_type_http_repr_comparator))
        return out

    @staticmethod
    def map_http_representations_to_dtos(http_representations: list) -> list:
        all_mime_types = list(MimeType)
        mime_type_dict = {x.value.get_http_representation(): x.value for x in all_mime_types}
        out = list()
        for hr in http_representations:
            mt = mime_type_dict.get(hr)
            if mt is None:
                raise ValueError(f"No mime type with http representation: {hr}")
            out.append(mt)
        return out

    @staticmethod
    def add_extension_by_mime_type_name(filename: str, dto: mime_type_dto.MimeTypeDto) -> str:
        if dto in [MimeType.MP4_VIDEO.value, MimeType.MP4_AUDIO.value]:
            return f"{filename}.{dto.get_extension_with_no_dot()}"
        if dto.__eq__(MimeType.WEBM_AUDIO.value):
            return f"{filename}-audio.{dto.get_extension_with_no_dot()}"
        if dto.__eq__(MimeType.WEBM_VIDEO.value):
            return f"{filename}.{dto.get_extension_with_no_dot()}"
        raise ValueError(f"Could not add extension for mime type {dto.get_http_representation()}")
