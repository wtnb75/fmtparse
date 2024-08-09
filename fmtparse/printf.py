# printf format
import functools
from typing import Optional
from collections.abc import Generator
from enum import Enum, auto
from .wellknown import printf_wellknown
from .common import Parsed, ParsedType


class FormatError(Exception):
    pass


class Pstate(Enum):
    normal = auto()
    percent = auto()
    index = auto()
    escape = auto()


def parse(s: str, conversion: str, modifier: str, index: Optional[str] = None, percent: str = "%") -> \
        Generator[Parsed, None, None]:
    """
    parse printf-style format
    """
    state: Pstate = Pstate.normal
    text_val, modifier_val, index_val = "", "", ""
    for c in s:
        if state == Pstate.normal:
            if c in percent:
                if text_val:
                    yield Parsed(ParsedType.text, text_val)
                    text_val, modifier_val, index_val = "", "", ""
                state = Pstate.percent
                continue
            elif c == '\\':
                state = Pstate.escape
                continue
            text_val += c
        elif state == Pstate.escape:
            state = Pstate.normal
            if c == 'n':
                text_val += "\n"
            elif c == "t":
                text_val += "\t"
            else:
                text_val += c
        elif state == Pstate.percent:
            if index and c == index[0]:
                state = Pstate.index
                continue
            elif c in modifier:
                modifier_val += c
                continue
            elif c in conversion:
                yield Parsed(ParsedType.variable, c, modifier_val or None, index_val or None)
                text_val, modifier_val, index_val = "", "", ""
                state = Pstate.normal
                continue
            raise FormatError(f"invalid conversion: {c}")
        elif state == Pstate.index:
            if c == index[-1]:
                state = Pstate.percent
                continue
            index_val += c
    if text_val:
        yield Parsed(ParsedType.text, text_val)


def parse_wk(s: str, mode: str) -> Generator[tuple[Optional[str], str, str], None, None]:
    yield from parse(s, *printf_wellknown[mode])


for k in printf_wellknown.keys():
    def _(s):
        return parse_wk(s, k)
    locals()[f"parse_{k}"] = functools.partial(parse_wk, mode=k)
