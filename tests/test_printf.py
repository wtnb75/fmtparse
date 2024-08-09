import unittest
import fmtparse.printf
from fmtparse.common import Parsed, ParsedType

simple_glibc = [
    ("%s %.2f %02x %12d", [
        Parsed(ParsedType.variable, "s"),
        Parsed(ParsedType.text, " "),
        Parsed(ParsedType.variable, "f", ".2"),
        Parsed(ParsedType.text, " "),
        Parsed(ParsedType.variable, "x", "02"),
        Parsed(ParsedType.text, " "),
        Parsed(ParsedType.variable, "d", "12")]),
    ("%s %%s %%%s", [
        Parsed(ParsedType.variable, "s"),
        Parsed(ParsedType.text, " "),
        Parsed(ParsedType.variable, "%"),
        Parsed(ParsedType.text, "s "),
        Parsed(ParsedType.variable, "%"),
        Parsed(ParsedType.variable, "s")]),
    ("%s%d%s", [
        Parsed(ParsedType.variable, "s"),
        Parsed(ParsedType.variable, "d"),
        Parsed(ParsedType.variable, "s")]),
]

simple_python = [
    ("hello %s %d %(hello)s", [
        Parsed(ParsedType.text, "hello "),
        Parsed(ParsedType.variable, "s"),
        Parsed(ParsedType.text, " "),
        Parsed(ParsedType.variable, "d"),
        Parsed(ParsedType.text, " "),
        Parsed(ParsedType.variable, "s", None, "hello")]),
    ("%()s %(%)s %(%%)s %(s)d", [
        Parsed(ParsedType.variable, "s"),
        Parsed(ParsedType.text, " "),
        Parsed(ParsedType.variable, "s", None, "%"),
        Parsed(ParsedType.text, " "),
        Parsed(ParsedType.variable, "s", None, "%%"),
        Parsed(ParsedType.text, " "),
        Parsed(ParsedType.variable, "d", None, "s")]),
]


class TestProstr(unittest.TestCase):
    def test_simple_python(self):
        for a, b in simple_python:
            with self.subTest(f"python: {b}", a=a, b=b):
                self.assertEqual(b, list(fmtparse.printf.parse_python(a)))

    def test_simple_glibc(self):
        for a, b in simple_glibc:
            with self.subTest(f"glibc: {b}", a=a, b=b):
                self.assertEqual(b, list(fmtparse.printf.parse_glibc(a)))
