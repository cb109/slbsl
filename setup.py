# :coding: utf-8

import setuptools

setuptools.setup(
    name="slbsl",
    version="0.1.6",
    description="Convert slashes in text on commandline or in clipboard.",
    long_description=open("README.rst").read(),
    keywords="slash, backslash, linux, unix, windows, conversion",
    url="https://cb109@bitbucket.org/cb109/slbsl.git",
    author="Christoph Buelter",
    author_email="c.buelter@arcor.de",
    packages=setuptools.find_packages(),
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

