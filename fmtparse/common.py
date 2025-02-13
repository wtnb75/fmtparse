from enum import Enum, auto
from typing import NamedTuple


class ParsedType(Enum):
    text = auto()
    variable = auto()


class Parsed(NamedTuple):
    ptype: ParsedType
    value: str
    option: str | None = None
    convert: str | None = None
