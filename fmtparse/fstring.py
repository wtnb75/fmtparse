# f-string format
from enum import Enum, auto
from collections.abc import Generator
from .common import Parsed, ParsedType


class Fstate(Enum):
    normal = auto()
    paren = auto()
    opts = auto()
    conv = auto()
    bslash = auto()


def parse(s: str, mode: str = r"{}:!") -> Generator[Parsed, None, None]:
    """
    parse f-string styled format
    """
    state: Fstate = Fstate.normal
    text_val, var_val, opt_val, conv_val = "", "", "", ""
    for c in s:
        if state == Fstate.normal:
            if c == mode[0]:
                state = Fstate.paren
                if text_val:
                    yield Parsed(ParsedType.text, text_val)
                text_val, var_val, opt_val, conv_val = "", "", "", ""
                continue
            text_val += c
            continue
        if state == Fstate.paren:
            if c == mode[1]:
                yield Parsed(ParsedType.variable, var_val, opt_val or None, conv_val or None)
                text_val, var_val, opt_val, conv_val = "", "", "", ""
                state = Fstate.normal
                continue
            if len(mode) >= 3 and c == mode[2]:
                state = Fstate.opts
                continue
            if len(mode) >= 4 and c == mode[3]:
                state = Fstate.conv
                continue
            var_val += c
            continue
        if state == Fstate.opts:
            if c == mode[1]:
                yield Parsed(ParsedType.variable, var_val, opt_val or None, conv_val or None)
                text_val, var_val, opt_val, conv_val = "", "", "", ""
                state = Fstate.normal
                continue
            if len(mode) >= 4 and c == mode[3]:
                state = Fstate.conv
                continue
            opt_val += c
            continue
        if state == Fstate.conv:
            if c == mode[1]:
                yield Parsed(ParsedType.variable, var_val, opt_val or None, conv_val or None)
                text_val, var_val, opt_val, conv_val = "", "", "", ""
                state = Fstate.normal
                continue
            if len(mode) >= 3 and c == mode[2]:
                state = Fstate.opts
                continue
            conv_val += c
            continue
    if text_val:
        yield Parsed(ParsedType.text, text_val)
    if var_val:
        yield Parsed(ParsedType.variable, var_val, opt_val or None, conv_val or None)
