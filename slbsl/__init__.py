"""
Convert paths from Windows to UNIX and vice versa.

This affects slashes vs backslashes, drive letters and escaping of
spaces and parentheses. Please note that the script is pretty dumb, so
make sure to give it a path, not arbitrary text.

If no text is given to the function (or shell script), it will take the
clipboard content as input. The result is printed to the commandline and
also stored to the clipboard.

"""
__all__ = ["sl", "bsl"]


import re
import sys

import pyperclip


colon = ":"
slash = "/"
backslash = "\\"
space = " "
openpar = "("
closepar = ")"


def _getCommandlineInput():
    args = sys.argv[1:]
    txt = " ".join(args) if args else None
    return txt


def _getClipboardContent():
    return str(pyperclip.paste())


def _setClipboardContent(txt):
    return pyperclip.copy(txt)


def _ensurePath(pth):
    pth = pth or _getCommandlineInput() or _getClipboardContent()
    if not pth:
        print ("ERROR - Could not get path from commandline "
               "or clipboard or it is empty.")
        sys.exit(1)
    return pth


def _convertWindowsDriveLetter(pth):
    original = pth
    pth = pth.replace(colon + backslash, slash)
    pth = pth.replace(colon + slash, slash)
    haschanged = pth != original
    if haschanged:
        pth = slash + pth
    return pth


def _escapeWindows(pth):
    for token in (space, openpar, closepar):
        pth = pth.replace(token, backslash + token)
    return pth


def _convertWindowsSlashes(pth):
    return pth.replace(backslash, slash)


def _convertUnixDriveLetter(pth):
    starts_with_unix_driveletter = r"(\/[a-zA-Z]\/)"
    match = re.match(starts_with_unix_driveletter, pth)
    if match:
        pth = pth[1] + colon + backslash + pth[3:]
    pth = pth.replace(colon + slash, colon + backslash)
    return pth


def _convertUnixSlashes(pth):
    return pth.replace(slash, backslash)


def _unescapeUnix(pth):
    for token in (space, openpar, closepar):
        pth = pth.replace(backslash + token, token)
    return pth


def _toWindows(pth):
    pth = _convertUnixDriveLetter(pth)
    pth = _convertUnixSlashes(pth)
    pth = _unescapeUnix(pth)
    _setClipboardContent(pth)
    return pth


def _toUnix(pth):
    pth = _convertWindowsDriveLetter(pth)
    pth = _convertWindowsSlashes(pth)
    pth = _escapeWindows(pth)
    _setClipboardContent(pth)
    return pth


def sl(pth=None):
    pth = _ensurePath(pth)
    return _toUnix(pth)


def bsl(pth=None):
    pth = _ensurePath(pth)
    return _toWindows(pth)