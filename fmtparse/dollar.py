import functools
from enum import Enum, auto
from collections.abc import Generator
from typing import Optional
from logging import getLogger
from .wellknown import dollar_wellknown
from .common import Parsed, ParsedType

_log = getLogger(__name__)


class Dstate(Enum):
    normal = auto()
    dollar = auto()
    dollar2 = auto()
    in_par = auto()
    in_opt = auto()
    bslash = auto()

# mode: '${}:'


def parse(s: str, mode: str, var_chars: str) -> Generator[Parsed, None, None]:
    """
    parse $variable styled format
    """
    state: Dstate = Dstate.normal
    text_val, dollar_val, opt_val = "", "", ""
    for c in s:
        _log.debug("char: %s, state=%s", repr(c), state)
        if state == Dstate.normal:
            if c == mode[0]:
                state = Dstate.dollar
                if text_val:
                    _log.debug("yield text %s", repr(text_val))
                    yield Parsed(ParsedType.text, text_val)
                    text_val, dollar_val, opt_val = "", "", ""
                continue
            if c == '\\':
                state = Dstate.bslash
                continue
            text_val += c
        elif state == Dstate.dollar:
            if c == mode[1]:
                state = Dstate.in_par
                continue
            state = Dstate.dollar2
            dollar_val += c
        elif state == Dstate.dollar2:
            if c not in var_chars:
                _log.debug("yield var %s %s", repr(dollar_val), repr(opt_val))
                yield Parsed(ParsedType.variable, dollar_val, opt_val or None)
                text_val, dollar_val, opt_val = "", "", ""
                if c == mode[0]:
                    state = Dstate.dollar
                else:
                    state = Dstate.normal
                    text_val = c
                continue
            dollar_val += c
        elif state == Dstate.in_par:
            if c == mode[2]:
                _log.debug("yield var{} %s %s", repr(dollar_val), repr(opt_val))
                yield Parsed(ParsedType.variable, dollar_val, opt_val or None)
                text_val, dollar_val, opt_val = "", "", ""
                state = Dstate.normal
                continue
            if len(mode) > 3 and c == mode[3]:
                state = Dstate.in_opt
                continue
            dollar_val += c
        elif state == Dstate.in_opt:
            if c == mode[2]:
                _log.debug("yield var{:} %s %s", repr(dollar_val), repr(opt_val))
                yield Parsed(ParsedType.variable, dollar_val, opt_val or None)
                text_val, dollar_val, opt_val = "", "", ""
                state = Dstate.normal
                continue
            opt_val += c
        elif state == Dstate.bslash:
            text_val += c
            state = Dstate.normal
    if text_val:
        _log.debug("yield-rest text %s", repr(text_val))
        yield Parsed(ParsedType.text, text_val)
    if dollar_val:
        _log.debug("yield-rest var %s %s", repr(dollar_val), repr(opt_val))
        yield Parsed(ParsedType.variable, dollar_val, opt_val or None)
    _log.debug("finished")


def parse_dr(s: str, mode: str) -> Generator[tuple[Optional[str], str, str], None, None]:
    yield from parse(s, *dollar_wellknown[mode])


for k in dollar_wellknown.keys():
    def _(s):
        return parse_dr(s, k)
    locals()[f"parse_{k}"] = functools.partial(parse_dr, mode=k)
