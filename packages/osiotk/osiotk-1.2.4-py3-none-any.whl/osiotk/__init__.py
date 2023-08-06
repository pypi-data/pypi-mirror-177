from typing import Callable, Optional, TypeVar
import os
from os import DirEntry
from getpass import getuser as __username
from collections import defaultdict as __defaultdict
import json as __json
from . import constants as __constants
from .objects import FWrite as __FW
from .path import abspath as __abspath
from .scan import scandir as __scandir

scandir = __scandir

T = TypeVar("T")

FilePredicate = Callable[[DirEntry], bool]
Path, Where = str, Optional[FilePredicate]


def __remove_path(__path: Path):
    path = __path.path if isinstance(__path, DirEntry) else __path
    if __exists(path, True):
        os.remove(path)


def __remove(__path: str, __is_abspath: bool, __where: Where):
    for file in __scandir(__path, __is_abspath, __where, None, False):
        __remove_path(file)


def __makedirs(__name: str, __is_abspath: bool, __exist_ok: bool):
    path = __abspath(__name, __is_abspath)
    if not __dir_exists(path, True):
        os.makedirs(path, exist_ok=__exist_ok)


def __mkfile(__name: str, __is_abspath: bool, __exist_ok: bool):
    path = __abspath(__name, __is_abspath)
    if not __file_exists(path, True):
        if __exist_ok:
            pdir = __parentdir(path, True)
            if not __dir_exists(pdir, True):
                __makedirs(pdir, True, __exist_ok)
            with open(
                path, "w+", errors=__constants.ERRORS, encoding=__constants.ENCODING
            ) as file:
                file.write("")
                file.close()
            # __writes(path, "", True, __constants.ERRORS, __constants.ENCODING, True)


def __filetree_paths(__ft: str, __parentdir: Optional[str], __indent: int) -> list[str]:
    paths, dirlog = [], __defaultdict(list[str])
    for line in (line for line in __ft.splitlines(keepends=False) if line):
        offset, path = len(line) - len(line.lstrip()), line.strip()
        dirlog[offset].append(path)
        while offset > 0:
            if dirlog[offset - __indent]:
                path = f"{dirlog[offset-__indent][-1]}/{path}"
            offset -= __indent
        if path:
            paths.append(path)
    if __parentdir is not None and __parentdir:
        for (i, path) in ((i, p) for (i, p) in enumerate(paths) if p == p.lstrip()):
            paths[i] = __join(__parentdir, path)
    return paths


def __mkfiletree(
    __ft: str, __overwrite_if_exists: bool, __parentdir: Optional[str], __indent: int
):
    ft_paths = __filetree_paths(__ft, __parentdir, __indent)
    dirpaths = set()

    for path in (p for p in ft_paths if not "." in basename(p)):
        subs = (p for p in ft_paths if p.startswith(path + "/"))
        if any((p != path for p in subs)):
            dirpaths.add(path)

    for dirpath in dirpaths:
        __mkdir(dirpath, False, True)

    for path in (path for path in ft_paths if not path in dirpaths):
        if __file_exists(path, False):
            if __overwrite_if_exists:
                __writes(
                    path, "", False, __constants.ERRORS, __constants.ENCODING, True
                )
        else:
            __mkfile(path, False, True)

    for path in ft_paths:
        if not __exists(path, False):
            print(f"error: path does not exist:{path}")


def __ext(__path: Path):
    path = __path.name if isinstance(__path, DirEntry) else __path
    return path.split(".")[-1] if "." in path else path


__system = lambda __command: os.system(command=__command)
__mkdir = __makedirs
__rmdir = lambda __path, __is_abspath: __system(
    f"rm -R {__abspath(__path,__is_abspath)}"
)
__join = lambda __a, *paths: os.path.join(__a, *paths)
__basename = lambda __name: __name.split("/")[-1] if "/" in __name else __name
__isabs = lambda __path: os.path.isabs(__path)
__isfile = lambda __path: os.path.isfile(__path)
__isdir = lambda __path: os.path.isdir(__path)
__islink = lambda __path: os.path.islink(__path)
__ctime = lambda __path: os.path.getctime(__path)
__atime = lambda __path: os.path.getatime(__path)
__mtime = lambda __path: os.path.getmtime(__path)
__size = lambda __path: os.path.getsize(__path)


def __parentdir(__name: str, __is_abspath: bool):
    result = __abspath(__name, __is_abspath)
    return "/".join(result.split("/")[:-1]) if "/" in result else result


def __safeabs(__name: str, __is_abspath: bool):
    return __name if __is_abspath and __isabs(__name) else __abspath(__name, False)


def __safepath(__name: str, __is_abspath: bool, __exist_ok: bool):
    path = __abspath(__name, __is_abspath)
    dirname = __parentdir(path, True)
    if not __dir_exists(dirname, True):
        os.makedirs(dirname, exist_ok=__exist_ok)
    if not __exists(path, True):
        __system(f"cd ~;touch {path};")
    return path


def __exists(__name: str, __is_abspath: bool):
    return os.path.exists(__safeabs(__name, __is_abspath))


def __file_exists(__name: str, __is_abspath: bool):
    path = __safeabs(__name, __is_abspath)
    return __exists(path, True) and __isfile(path)


def __dir_exists(__name: str, __is_abspath: bool):
    path = __safeabs(__name, __is_abspath)
    return __exists(path, True) and __isdir(path)


def __writes(__fw: __FW):
    path = __safepath(__fw.name, __fw.is_abspath, __fw.exist_ok)
    with open(path, mode="w+", errors=__fw.errors, encoding=__fw.encoding) as file:
        file.write(__fw.content)
        file.close()


def __writeb(__fw: __FW):
    path = __safepath(__fw.name, __fw.is_abspath, __fw.exist_ok)
    with open(path, "w+", errors=__fw.errors, encoding=__fw.encoding) as file:
        file.write(__fw.content)
        file.close()


def __writejson(__fw: __FW):
    __fw.content = __json.dumps(__fw.content, indent=__fw.indent)
    return __writes(__fw)


def __write(__fw: __FW):
    return (__writes if isinstance(__fw.content, str) else __writejson)(__fw)


def __read_or_none(func):
    def inner(*a, **b):
        try:
            result = func(*a, **b)
        except Exception:
            result = None
        return result

    return inner


@__read_or_none
def __reads(__name: str, __is_abspath: bool):
    path = __abspath(__name, __is_abspath)
    result = None
    with open(path, mode="r") as file:
        result = str(file.read())
    return result


@__read_or_none
def __readb(__name: str, __is_abspath: bool):
    path = __abspath(__name, __is_abspath)
    with open(path, mode="rb") as file:
        result = file.read()
    return result


@__read_or_none
def __readjson(__name: str, __is_abspath: bool):
    return __json.loads(__reads(__name, __is_abspath))


@__read_or_none
def __readlines(
    __name: str,
    __is_abspath: bool,
    __keepends: bool,
    __where: Optional[Callable[[str], bool]],
):
    fstr = __reads(__name, __is_abspath)
    result = fstr.splitlines(keepends=__keepends)
    if __where is not None:
        result = [line for line in result if __where(line)]
    return result


def join(__a: str, *paths):
    return __join(__a, *paths)


def isfile(__path: str):
    return __isfile(__path)


def isdir(__path: str):
    return __isdir(__path)


def islink(__path: str):
    return __islink(__path)


def isabs(__path: str):
    return __isabs(__path)


def abspath(__path: str, is_abspath: bool = False):
    return __abspath(__path, is_abspath)


def atime(__path: str):
    """access time; time last accessed"""
    return __atime(__path)


def ctime(__path: str):
    """created time ; time file is created at"""
    return __ctime(__path)


def mtime(__path: str):
    """modified time; time file was last modified"""
    return __mtime(__path)


def size(__path: str):
    """file size"""
    return __size(__path)


def exists(__name: str, is_abspath: bool = False):
    return __exists(__name, is_abspath)


def file_exists(__name: str, is_abspath: bool = False):
    return __file_exists(__name, is_abspath)


def dir_exists(__name: str, is_abspath: bool = False):
    return __dir_exists(__name, is_abspath)


def basename(__name: str):
    return __basename(__name)


def parentdir(__name: str, is_abspath: bool = False):
    return __parentdir(__name, is_abspath)


def writes(
    __name: str,
    content: str,
    is_abspath: bool = False,
    errors: str = __constants.ERRORS,
    encoding: str = __constants.ENCODING,
    exist_ok: bool = True,
):
    return __writes(__FW(__name, content, is_abspath, errors, encoding, exist_ok, 0))


def writeb(
    __name: str,
    content: bytes,
    is_abspath: bool = False,
    errors: str = __constants.ERRORS,
    encoding: str = __constants.ENCODING,
    exist_ok: bool = True,
):
    return __writeb(__FW(__name, content, is_abspath, errors, encoding, exist_ok, 0))


def writejson(
    __name: str,
    content,
    indent: int = 4,
    is_abspath: bool = False,
    errors: str = __constants.ERRORS,
    encoding: str = __constants.ENCODING,
    exist_ok: bool = True,
):
    fw = __FW(__name, content, is_abspath, errors, encoding, exist_ok, indent)
    return __writejson(fw)


def write(
    __name: str,
    content,
    indent: int = 4,
    is_abspath: bool = False,
    errors: str = __constants.ERRORS,
    encoding: str = __constants.ENCODING,
    exist_ok: bool = True,
):
    fw = __FW(__name, content, is_abspath, errors, encoding, exist_ok, indent)
    return __write(fw)


def reads(__name: str, is_abspath: bool = False):
    return __reads(__name, is_abspath)


def readb(__name: str, is_abspath: bool = False):
    return __readb(__name, is_abspath)


def readjson(__name: str, is_abspath: bool = False):
    return __readjson(__name, is_abspath)


def readlines(
    __name: str,
    is_abspath: bool = False,
    keepends: bool = False,
    where: Optional[Callable[[str], bool]] = None,
):
    return __readlines(__name, is_abspath, keepends, where)


def system(__command: str):
    return __system(__command)


def makedirs(__name: str, is_abspath: bool = False, exist_ok: bool = True):
    return __makedirs(__name, is_abspath, exist_ok)


def mkfile(__name: str, is_abspath: bool = False, exist_ok: bool = True):
    return __mkfile(__name, is_abspath, exist_ok)


def mkdir(__name: str, is_abspath: bool = False, exist_ok: bool = True):
    return __mkdir(__name, is_abspath, exist_ok)


def mkfiletree(
    __ft: str,
    overwrite_if_exists: bool = False,
    parentdir: Optional[str] = None,
    indent: int = 4,
):
    return __mkfiletree(__ft, overwrite_if_exists, parentdir, indent)


def mk_filetree(
    __ft: str,
    overwrite_if_exists: bool = False,
    parentdir: Optional[str] = None,
    indent: int = 4,
):
    """soon to be deprecated"""
    return __mkfiletree(__ft, overwrite_if_exists, parentdir, indent)


def remove_path(__path: Path):
    return __remove_path(__path)


def remove(
    __path: str,
    is_abspath: bool = False,
    where: Optional[Callable[[DirEntry], bool]] = None,
):
    return __remove(__path, is_abspath, where)


def username():
    return __username()


def ext(__path: Path):
    return __ext(str(__path))


def rmdir(__path: str, is_abspath: bool = True):
    return __rmdir(__path, is_abspath)
