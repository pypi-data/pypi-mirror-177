from typing import Callable, Optional, Any
from os import DirEntry
from enum import Enum
from dataclasses import dataclass, field


@dataclass(frozen=False, order=True)
class DirScan:
    class ScanType(Enum):
        FILES = 1
        DIRS = 2
        ALL = 3

    path: str = field(default="")
    is_abspath: bool = field(default=False)
    where: Optional[Callable[[DirEntry], bool]] = field(default=None)
    key: Optional[Callable[[DirEntry], Any]] = field(default=None)
    reverse: bool = field(default=False)
    recursive: bool = field(default=False)
    scan_type: ScanType = field(default=ScanType.ALL)
    fh: Optional[Callable] = field(default=None)


@dataclass(frozen=False, order=True)
class FWrite:
    name: str = field(init=True)
    content: str = field(init=True)
    is_abspath: bool = field(init=True)
    errors: str = field(init=True)
    encoding: str = field(init=True)
    exist_ok: bool = field(init=True)
    indent: int = field(init=True)
