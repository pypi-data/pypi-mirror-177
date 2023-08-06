import os

__isabs = lambda __path: os.path.isabs(__path)


def __abspath(__path: str, __is_abspath: bool):
    return __path if __is_abspath and __isabs(__path) else os.path.abspath(__path)


def abspath(__path: str, __is_abspath: bool):
    return __abspath(__path, __is_abspath)
