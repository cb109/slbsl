# :coding: utf-8

import setuptools

setuptools.setup(
    name="slbsl",
    version="0.2.0",
    description="Convert paths from Windows to UNIX and vice versa.",
    long_description=open("README.rst").read(),
    keywords="slash, backslash, linux, unix, windows, conversion",
    url="https://github.com/cb109/slbsl.git",
    author="Christoph Buelter",
    author_email="info@cbuelter.de",
    py_modules=["slbsl"],
    install_requires=[
        "pyperclip"
    ],
    entry_points={
        "console_scripts": [
            "sl=slbsl:sl",
            "bsl=slbsl:bsl"
        ],
    }
)

