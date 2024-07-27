import unittest
import glob
import os
import subprocess
import importlib

simple_p = [
    ("hello %s %d %(hello)s",
     [(None, "hello ", None), ("s", '', ''), (None, " ", None), ("d", '', ''), (None, " ", None), ("s", '', 'hello')]),
    ("%s %.2f %02x %>12d",
     [("s", ''), (None, " "), ("f", '.2'), (None, " "), ("x", "02"), (None, " "), ("d", ">12")]),
    ("%s %%s %%%s",
     [("s", ''), (None, " "), (None, "%s "), (None, "%"), ("s", "")]),
    ("%()s %(%)s %(%%)s %(s)d",
     [("s", ''), (None, " "), ("s", "%"), (None, " "), ("s", "%%"), (None, " "), ("d", "s")]),
]


class TestCProstr(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.call(["cythonize", "-i", "--3str",
                        os.path.join(os.path.dirname(__file__), "..", "fmtparse", "printf_bin.pyx")],
                        env=dict(CFLAGS="-DCYTHON_TRACE=1", **os.environ))
        mod = importlib.import_module("fmtparse.printf_bin")
        cls.parse_python = staticmethod(mod.parse_python)

    @classmethod
    def tearDownClass(cls):
        if os.getenv("CYTHON_CLEANUP", None):
            for k in glob.glob(os.path.join(os.path.dirname(__file__), "..", "fmtparse", "printf_bin.c*")):
                os.unlink(k)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simple(self):
        for a, b in simple_p:
            self.assertEqual(b, list(self.parse_python(a)))


class TestProstr(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        mod = importlib.import_module("fmtparse.printf_py")
        cls.parse_python = staticmethod(mod.parse_python)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simple(self):
        for a, b in simple_p:
            self.assertEqual(b, list(self.parse_python(a)))
