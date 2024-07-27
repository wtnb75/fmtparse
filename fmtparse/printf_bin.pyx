import functools
from .printf import FormatError
from .wellknown import printf_wellknown

ctypedef enum Pstate:
    p_normal, p_percent, p_option, p_index, p_escape

cdef class parse:
    cdef:
        str s
        str conversion
        str modifier
        str text_val
        str modifier_val
        str index_val
        str percent
        str index
        int state
        int cur

    def __cinit__(self, str s not None, str conversion not None, str modifier not None,
                  str index = "", str percent = "%"):
        self.s = s
        self.cur = 0
        self.state = Pstate.p_normal
        self.text_val = ""
        self.modifier_val = ""
        self.conversion = conversion
        self.modifier = modifier
        self.percent = percent or "%"
        self.index = index or ""

    def __iter__(self):
        return self

    def __next__(self):
        while self.cur < len(self.s):
            c = self.s[self.cur]
            self.cur += 1
            if self.state == Pstate.p_normal:
                if c in self.percent:
                    self.state = Pstate.p_percent
                    self.modifier_val = ""
                    self.index_val = ""
                    if self.text_val:
                        tval = self.text_val
                        self.text_val = ""
                        return None, tval, None
                    continue
                elif c == '\\':
                    self.state = Pstate.p_escape
                    continue
                self.text_val += c
            elif self.state == Pstate.p_escape:
                self.state = Pstate.p_normal
                if c == 'n':
                    self.text_val += "\n"
                elif c == "t":
                    self.text_val += "\t"
                else:
                    self.text_val += c
            elif self.state == Pstate.p_percent:
                if self.index and c == self.index[0]:
                    self.state = Pstate.p_index
                    continue
                elif c in self.percent:
                    self.state = Pstate.p_normal
                    self.text_val = c
                    continue
                elif c in self.modifier:
                    self.modifier_val += c
                    continue
                elif c in self.conversion:
                    mod_val = self.modifier_val
                    idx_val = self.index_val
                    self.modifier_val = ""
                    self.index_val = ""
                    self.text_val = ""
                    self.state = Pstate.p_normal
                    return c, mod_val, idx_val
                else:
                    raise FormatError(f"invalid conversion: {c}")
            elif self.state == Pstate.p_index:
                if c == self.index[-1]:
                    self.state = Pstate.p_percent
                    continue
                self.index_val += c

        if self.text_val:
            tval = self.text_val
            self.text_val = ""
            return None, tval, None
        raise StopIteration

def parse_wk(s: str, mode: str):
    return parse(s, *printf_wellknown[mode])

for k in printf_wellknown.keys():
    def _(s):
        return parse_wk(s, k)
    locals()[f"parse_{k}"] = functools.partial(parse_wk, mode=k)
