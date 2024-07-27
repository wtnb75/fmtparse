import unittest
import fmtparse.printf
try:
    import fmtparse.printf_bin
    no_binary = False
except ImportError:
    no_binary = True

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
    @classmethod
    def setUpClass(cls):
        cls.mod = fmtparse.printf

    def test_simple_python(self):
        for a, b in simple_python:
            self.assertEqual(b, list(self.mod.parse_python(a)))

    def test_simple_glibc(self):
        for a, b in simple_glibc:
            self.assertEqual(b, list(self.mod.parse_glibc(a)))


@unittest.skipIf(no_binary, "no cython binary")
class TestProstr_cython(TestProstr):
    @classmethod
    def setUpClass(cls):
        cls.mod = fmtparse.printf_bin
