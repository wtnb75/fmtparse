from pathlib import Path
from setuptools import setup, Extension

extras_require = {
    x.stem.split("-", 1)[-1]: x.read_text().splitlines()
    for x in Path(__file__).parent.glob("requirements-*.txt")
}

setup(
    install_requires=Path("requirements.txt").read_text().splitlines(),
    setup_requires=["setuptools>=18.0", "cython"],
    ext_modules=[
        Extension("fmtparse.printf", sources=["fmtparse/printf.py"]),
    ],
    extras_require=extras_require
)
