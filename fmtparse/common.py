from typing import NamedTuple, Optional
from enum import Enum, auto


class ParsedType(Enum):
    text = auto()
    variable = auto()


class Parsed(NamedTuple):
    ptype: ParsedType
    value: str
    option: Optional[str] = None
    convert: Optional[str] = None
