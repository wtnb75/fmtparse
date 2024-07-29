import unittest
import fmtparse.printf

simple_glibc = [
    ("%s %.2f %02x %12d",
     [("s", '', ''), (None, " ", None), ("f", '.2', ''), (None, " ", None),
      ("x", "02", ""), (None, " ", None), ("d", "12", "")]),
    ("%s %%s %%%s",
     [('s', '', ''), (None, ' ', None), ('%', '', ''),
      (None, 's ', None), ('%', '', ''), ('s', '', '')]),
]

simple_python = [
    ("hello %s %d %(hello)s",
     [(None, "hello ", None), ("s", '', ''), (None, " ", None),
      ("d", '', ''), (None, " ", None), ("s", '', 'hello')]),
    ("%()s %(%)s %(%%)s %(s)d",
     [("s", '', ''), (None, " ", None), ("s", "", "%"), (None, " ", None),
      ("s", "", "%%"), (None, " ", None), ("d", "", "s")]),
]


class TestProstr(unittest.TestCase):
    def test_simple_python(self):
        for a, b in simple_python:
            self.assertEqual(b, list(fmtparse.printf.parse_python(a)))

    def test_simple_glibc(self):
        for a, b in simple_glibc:
            self.assertEqual(b, list(fmtparse.printf.parse_glibc(a)))
