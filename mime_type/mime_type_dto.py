class MimeTypeDto:
    def __init__(self, http_representation: str, extension_with_no_dot: str):
        self.__extension_with_no_dot = extension_with_no_dot
        self.__http_representation = http_representation

    def get_extension_with_no_dot(self):
        return self.__extension_with_no_dot

    def get_http_representation(self):
        return self.__http_representation

    def get_subtype(self):
        return self.__http_representation.split('/')[1]

    def get_type(self):
        return self.__http_representation.split('/')[0]

    def __eq__(self, obj):
        return isinstance(obj, MimeTypeDto) and obj.__http_representation == self.__http_representation

    def __str__(self):
        return f"{'{'}ext = {self.get_extension_with_no_dot()}," \
               f" http_repr = {self.get_http_representation()}{'}'}"

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        http_repr = hash(self.__http_representation)
        ext = hash(self.__extension_with_no_dot)
        return 7 * http_repr + ext * 19 + 13
