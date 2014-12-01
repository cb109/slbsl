"""slbsl - slash & backslash conversion

Provides two functions to convert slashes/backslashes in text.
If no text is given to the function (or shell script), it will
take the clipboard content as input. The result is always stored
to the clipboard.

"""
__all__ = ["sl", "bsl"]

import sys

import pyperclip


def getCommandlineInput():
    args = sys.argv[1:]
    txt = " ".join(args) if args else None
    return txt


def getClipboardContent():
    return str(pyperclip.paste())


def setClipboardContent(txt):
    return pyperclip.copy(txt)


def convert(token, replacement, txt):
    txt = txt or getCommandlineInput() or getClipboardContent()
    if not txt:
        return False
    result = txt.replace(token, replacement)
    return setClipboardContent(result)


def sl(txt=None):
    return convert("\\", "/", txt)


def bsl(txt=None):
    return convert("/", "\\", txt)

