from typing import Callable, Optional, TypeVar, Iterable, Generator
import os
from ..objects import DirScan as DS
from ..path import abspath as __abspath

T = TypeVar("T")

FilePredicate = Callable[[os.DirEntry], bool]
Path, Where = str, Optional[FilePredicate]


__FILES = DS.ScanType.FILES
__ALL = DS.ScanType.ALL
__DIRS = DS.ScanType.DIRS


def __generator(__iter: Iterable[T]) -> Generator[T, None, None]:
    for i in __iter:
        yield i


def __reversed_generator(__iter: Iterable[T]) -> Generator[T, None, None]:
    return __generator(reversed(__iter))


def __recursive_filehandler(__ds: DS):
    st = __ds.scan_type
    if st == __ALL:

        def handle_file(__file: os.DirEntry):
            if __file.is_file():
                yield str(__file.path)
            elif __file.is_dir():
                path = str(__file.path)
                yield path

                for result in __recursivescan_base(path, __ds):
                    yield str(result)

    elif st == __DIRS:

        def handle_file(__file: os.DirEntry):
            if __file.is_dir():
                path = str(__file.path)
                yield path
                for result in __recursivescan_base(path, __ds):
                    yield str(result)

    elif st == __FILES:

        def handle_file(__file: os.DirEntry):
            if __file.is_file():
                yield str(__file.path)
            elif __file.is_dir():
                path = str(__file.path)
                for result in __recursivescan_base(path, __ds):
                    yield str(result)

    return handle_file


def __recursivescan_base(__path: str, __ds: DS):
    if __ds.fh is None:
        handle_file = __recursive_filehandler(__ds)
        where = __ds.where
        if where is not None:
            hf = handle_file

            def file_handler(__file):
                for p in hf(__file):
                    if where(p):
                        yield p

            handle_file = file_handler
        __ds.fh = handle_file

    for file in os.scandir(__path):
        for value in __ds.fh(file):
            yield value


def __scan_base(__ds: DS):
    result = (file for file in os.scandir(__ds.path))
    if __ds.where is not None:
        result = (file for file in result if __ds.where(file))
    if __ds.key is not None:
        result = list(result)
        result.sort(key=__ds.key)
    st = __ds.scan_type
    if st == __ALL:

        def handle_file(__file: os.DirEntry):
            if __file.is_file():
                yield str(__file.path)
            elif __file.is_dir():
                yield str(__file.path)

    elif st == __FILES:

        def handle_file(__file: os.DirEntry):
            if __file.is_file():
                yield str(__file.path)

    elif st == __DIRS:

        def handle_file(__file: os.DirEntry):
            if __file.is_dir():
                yield str(__file.path)

    for file in result:
        for path in handle_file(file):
            yield path


def __generate_recursive_dirscan(__ds: DS):
    return __generator(__recursivescan_base(__ds.path, __ds))


def __generate_dirscan(__ds: DS):
    return __generator(__scan_base(__ds))


def __scandir(__ds: DS):
    __ds.path = __abspath(__ds.path, __ds.is_abspath)
    result = (__generate_recursive_dirscan if __ds.recursive else __generate_dirscan)(
        __ds
    )
    if __ds.reverse:
        result = __reversed_generator(result)
    return result


def scandir(
    __path: str,
    is_abspath: bool = False,
    where: Where = None,
    key: Optional[Callable[[os.DirEntry], T]] = None,
    reverse: bool = False,
    recursive: bool = False,
    scan_type: str = "all",
):
    return __scandir(
        DS(
            __path,
            is_abspath,
            where,
            key,
            reverse,
            recursive,
            DS.ScanType[scan_type.upper()],
        )
    )
