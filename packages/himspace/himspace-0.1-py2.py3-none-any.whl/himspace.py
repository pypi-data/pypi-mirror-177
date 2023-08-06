from pathlib import Path as libpath
from os import stat, walk


def getspace(path):
    obj = libpath(path)
    if obj.is_file():
        info = stat(path, follow_symlinks=False)  # follow_symlinks: 符号链接, 须设为False
        return info.st_size
    if obj.is_dir():
        tatal = 0
        for bpath, dirs, files in walk(path):
            for file in files:
                fpath = f"{bpath}/{file}"
                tatal += stat(fpath, follow_symlinks=False).st_size
        return tatal