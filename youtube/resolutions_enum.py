from enum import Enum


class Resolution(Enum):
    SMALLEST = '144p'
    VERY_SMALL = '240p'
    SMALL = '360p'
    SD = '480p'
    HD = '720p'
    FHD = '1080p'
    QHD = '1440p'
    TWO_K = '1080p'
    FOUR_K = '2160p'
    EIGHT_K = '4320p'

    @staticmethod
    def get_available_resolutions():
        out = []
        for e in list(Resolution):
            out.append(e.name)
        return out

    @staticmethod
    def from_name(name: str):
        if name is None:
            return None
        for e in list(Resolution):
            if e.name == name.upper():
                return e
        raise ValueError(f"No such resolution: {name}")
