import os
import pathlib
from uuid import UUID


def get_downloads_path() -> str:
    if os.name == 'nt':
        import ctypes

        # ctypes GUID copied from MSDN sample code
        class GUID(ctypes.Structure):
            _fields_ = [
                ("Data1", ctypes.wintypes.DWORD),
                ("Data2", ctypes.wintypes.WORD),
                ("Data3", ctypes.wintypes.WORD),
                ("Data4", ctypes.wintypes.BYTE * 8)
            ]

            def __init__(self, uuidstr):
                uuid = UUID(uuidstr)
                ctypes.Structure.__init__(self)
                self.Data1, self.Data2, self.Data3, self.Data4[0], self.Data4[1], rest = uuid.fields
                for i in range(2, 8):
                    self.Data4[i] = rest >> (8 - i - 1) * 8 & 0xff

        SHGetKnownFolderPath = ctypes.windll.shell32.SHGetKnownFolderPath
        SHGetKnownFolderPath.argtypes = [
            ctypes.POINTER(GUID), ctypes.wintypes.DWORD,
            ctypes.wintypes.HANDLE, ctypes.POINTER(ctypes.c_wchar_p)
        ]

        def _get_known_folder_path(uuidstr):
            pathptr = ctypes.c_wchar_p()
            guid = GUID(uuidstr)
            if SHGetKnownFolderPath(ctypes.byref(guid), 0, 0, ctypes.byref(pathptr)):
                raise ctypes.WinError()
            return pathptr.value

        FOLDERID_Download = '{374DE290-123F-4565-9164-39C4925E467B}'

        return _get_known_folder_path(FOLDERID_Download)
    else:
        home = os.path.expanduser("~")
        return os.path.join(home, "Downloads")


def make_dirs_recursively(path):
    os.makedirs(path, exist_ok=True)


def get_abs_path(path):
    return os.path.abspath(path)


def get_file_name_without_directory(filename):
    return pathlib.Path(filename).stem


def delete_file(path):
    os.remove(path)
