import unittest
import fmtparse.dollar
import fmtparse.wellknown

simple_d = [
    (r"hello $name", [("text", "hello ", None), ("var", "name", '')]),
    (r"$abc$def$hij", [("var", "abc", ""), ("var", "def", ''), ("var", "hij", "")]),
    (r"abc $def $hij klm${op}qrstu", [
        ("text", "abc ", None), ("var", "def", ""), ("text", " ", None), ("var", "hij", ""),
        ("text", " klm", None), ("var", "op", ""), ("text", "qrstu", None)]),
    (r"$def $hij klm${op-hello} $world", [
        ("var", "def", ""), ("text", " ", None), ("var", "hij", ""), ("text", " klm", None),
        ("var", "op", "hello"), ("text", " ", None), ("var", "world", "")]),
    (r"${hello-world} ${xyz-abc}", [
        ("var", "hello", "world"), ("text", " ", None), ("var", "xyz", "abc")]),
]


class TestDollar(unittest.TestCase):
    def test_simple(self):
        for input, expected in simple_d:
            output = list(fmtparse.dollar.parse_envsubst(input))
            self.assertEqual(expected, output, f"input: {input}")
