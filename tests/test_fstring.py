import unittest
import fmtparse.fstring
import fmtparse.wellknown

simple_f = [
    (r"hello {name}", [("text", "hello ", None, None), ("var", "name", "", "")]),
    (r"{abc}{def}{hij}", [("var", "abc", "", ""), ("var", "def", "", ""), ("var", "hij", "", "")]),
    (r"abc {def} {hij} klm{op}qrstu", [
        ("text", "abc ", None, None), ("var", "def", "", ""), ("text", " ", None, None),
        ("var", "hij", "", ""), ("text", " klm", None, None), ("var", "op", "", ""),
        ("text", "qrstu", None, None)]),
    (r"{def} {hij} klm{op:hello!r} {world}", [
        ("var", "def", "", ""), ("text", " ", None, None), ("var", "hij", "", ""),
        ("text", " klm", None, None), ("var", "op", "hello", "r"), ("text", " ", None, None),
        ("var", "world", "", "")]),
    (r"{hello:world} {xyz!abc}", [
        ("var", "hello", "world", ""), ("text", " ", None, None), ("var", "xyz", "", "abc")]),
]


class TestFstring(unittest.TestCase):
    def test_simple(self):
        for input, expected in simple_f:
            with self.subTest(f"fstr {input}", input=input, expected=expected):
                output = list(fmtparse.fstring.parse(input, "{}:!"))
                self.assertEqual(expected, output, f"input: {input}")
