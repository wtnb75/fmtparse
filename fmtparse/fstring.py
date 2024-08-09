# f-string format
from enum import Enum, auto
from typing import Optional
from collections.abc import Generator


class Fstate(Enum):
    normal = auto()
    paren = auto()
    opts = auto()
    conv = auto()
    bslash = auto()

# mode: "{}:!"


def parse(s: str, mode: str) -> Generator[tuple[str, str, Optional[str], Optional[str]], None, None]:
    state: Fstate = Fstate.normal
    text_val, var_val, opt_val, conv_val = "", "", "", ""
    for c in s:
        if state == Fstate.normal:
            if c == mode[0]:
                state = Fstate.paren
                if text_val:
                    yield "text", text_val, None, None
                text_val, var_val, opt_val, conv_val = "", "", "", ""
                continue
            text_val += c
            continue
        if state == Fstate.paren:
            if c == mode[1]:
                yield "var", var_val, opt_val, conv_val
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
                yield "var", var_val, opt_val, conv_val
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
                yield "var", var_val, opt_val, conv_val
                text_val, var_val, opt_val, conv_val = "", "", "", ""
                state = Fstate.normal
                continue
            if len(mode) >= 3 and c == mode[2]:
                state = Fstate.opts
                continue
            conv_val += c
            continue
    if text_val:
        yield "text", text_val, None, None
    if var_val:
        yield "var", var_val, opt_val, conv_val
