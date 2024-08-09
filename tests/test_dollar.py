import unittest
import fmtparse.dollar
import fmtparse.wellknown
from fmtparse.common import Parsed, ParsedType

simple_d = [
    (r"hello $name", [
        Parsed(ParsedType.text, "hello "),
        Parsed(ParsedType.variable, "name")]),
    (r"$abc$def$hij", [
        Parsed(ParsedType.variable, "abc"),
        Parsed(ParsedType.variable, "def"),
        Parsed(ParsedType.variable, "hij")]),
    (r"abc $def $hij klm${op}qrstu", [
        Parsed(ParsedType.text, "abc "),
        Parsed(ParsedType.variable, "def"),
        Parsed(ParsedType.text, " "),
        Parsed(ParsedType.variable, "hij"),
        Parsed(ParsedType.text, " klm"),
        Parsed(ParsedType.variable, "op"),
        Parsed(ParsedType.text, "qrstu")]),
    (r"$def $hij klm${op-hello} $world", [
        Parsed(ParsedType.variable, "def"),
        Parsed(ParsedType.text, " "),
        Parsed(ParsedType.variable, "hij"),
        Parsed(ParsedType.text, " klm"),
        Parsed(ParsedType.variable, "op", "hello"),
        Parsed(ParsedType.text, " "),
        Parsed(ParsedType.variable, "world")]),
    (r"${hello-world} ${xyz-abc}", [
        Parsed(ParsedType.variable, "hello", "world"),
        Parsed(ParsedType.text, " "),
        Parsed(ParsedType.variable, "xyz", "abc")]),
]


class TestDollar(unittest.TestCase):
    def test_simple(self):
        for input, expected in simple_d:
            with self.subTest(f"dollar {input}", input=input, expected=expected):
                output = list(fmtparse.dollar.parse_envsubst(input))
                self.assertEqual(expected, output, f"input: {input}")
