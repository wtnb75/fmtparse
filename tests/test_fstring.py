import unittest
import fmtparse.fstring
import fmtparse.wellknown
from fmtparse.common import Parsed, ParsedType

simple_f = [
    (r"hello {name}", [
        Parsed(ParsedType.text, "hello "),
        Parsed(ParsedType.variable, "name")]),
    (r"{abc}{def}{hij}", [
        Parsed(ParsedType.variable, "abc"),
        Parsed(ParsedType.variable, "def"),
        Parsed(ParsedType.variable, "hij")]),
    (r"abc {def} {hij} klm{op}qrstu", [
        Parsed(ParsedType.text, "abc "),
        Parsed(ParsedType.variable, "def"),
        Parsed(ParsedType.text, " "),
        Parsed(ParsedType.variable, "hij"),
        Parsed(ParsedType.text, " klm"),
        Parsed(ParsedType.variable, "op"),
        Parsed(ParsedType.text, "qrstu")]),
    (r"{def} {hij} klm{op:hello!r} {world}", [
        Parsed(ParsedType.variable, "def"),
        Parsed(ParsedType.text, " "),
        Parsed(ParsedType.variable, "hij"),
        Parsed(ParsedType.text, " klm"),
        Parsed(ParsedType.variable, "op", "hello", "r"),
        Parsed(ParsedType.text, " "),
        Parsed(ParsedType.variable, "world")]),
    (r"{hello:world} {xyz!abc}", [
        Parsed(ParsedType.variable, "hello", "world"),
        Parsed(ParsedType.text, " "),
        Parsed(ParsedType.variable, "xyz", None, "abc")]),
]


class TestFstring(unittest.TestCase):
    def test_simple(self):
        for input, expected in simple_f:
            with self.subTest(f"fstr {input}", input=input, expected=expected):
                output = list(fmtparse.fstring.parse(input, "{}:!"))
                self.assertEqual(expected, output, f"input: {input}")
