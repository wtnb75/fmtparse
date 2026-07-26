import fmtparse.dollar
import fmtparse.fstring
import fmtparse.printf


def test_printf_glibc(benchmark):
    fmt = "hello %s world %d\n"
    benchmark(lambda: list(fmtparse.printf.parse_glibc(fmt)))


def test_printf_python(benchmark):
    fmt = "hello %(name)s world %(value)d\n"
    benchmark(lambda: list(fmtparse.printf.parse_python(fmt)))


def test_dollar_envsubst(benchmark):
    fmt = "hello $abc world ${def}\n"
    benchmark(lambda: list(fmtparse.dollar.parse_envsubst(fmt)))


def test_fstring(benchmark):
    fmt = "hello {abc} world {def}\n"
    benchmark(lambda: list(fmtparse.fstring.parse(fmt)))
