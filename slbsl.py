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
    """Returns commandline args as space-separated string."""
    args = sys.argv[1:]
    txt = " ".join(args) if args else None
    return txt


def _getClipboardContent():
    """Returns the content of the Windows clipboard."""
    return str(pyperclip.paste())


def _setClipboardContent(txt):
    """Sets the Windows clipboard content to the given text."""
    return pyperclip.copy(txt)


def _ensurePath(pth):
    """Tries to get pth either as given, or from commandline or the
    clipboard. If none of these source provide input, bail out."""
    pth = pth or _getCommandlineInput() or _getClipboardContent()
    if not pth:
        print ("ERROR - Could not get path from commandline "
               "or clipboard or it is empty.")
        sys.exit(1)
    return pth


def _convertWindowsDriveLetter(pth):
    """Converts 'C:\' to '/C/'. Handles wrapping quotation marks."""
    original = pth
    pth = pth.replace(colon + backslash, slash)
    pth = pth.replace(colon + slash, slash)
    haschanged = pth != original
    if haschanged:
        # Inject slash before driveletter.
        firstslash_index = pth.find(slash)
        if firstslash_index:
            driveletter_index = firstslash_index - 1
            pth = pth[:driveletter_index] + slash + pth[driveletter_index:]
    return pth


def _escapeWindows(pth):
    """Escapes certain characters in pth with a backslash."""
    for token in (space, openpar, closepar):
        pth = pth.replace(token, backslash + token)
    return pth


def _convertWindowsSlashes(pth):
    """Replaces all backslashes in pth with slashes."""
    return pth.replace(backslash, slash)


def _convertUnixDriveLetter(pth):
    """Converts '/C/' to 'C:\'. Handles wrapping quotation marks."""
    starts_with_unix_driveletter = r"([\"\']*)(\/)(?P<drive>[a-zA-Z])(\/)"
    match = re.match(starts_with_unix_driveletter, pth)
    if match:
        drive = match.group("drive")
        drive_index = pth.find(drive)
        # Drop the leading slash, while keeping any quotation marks.
        pth = (pth[:drive_index - 1] +
               drive + colon + backslash +
               pth[drive_index + 2:])
    pth = pth.replace(colon + slash, colon + backslash)
    return pth


def _convertUnixSlashes(pth):
    """Replaces all slashes in pth with backslashes."""
    return pth.replace(slash, backslash)


def _unescapeUnix(pth):
    """Removes backslashes in front of certain characters in pth."""
    for token in (space, openpar, closepar):
        pth = pth.replace(backslash + token, token)
    return pth


def _toWindows(pth):
    """Converts the given Unix path to Windows convention."""
    pth = _convertUnixDriveLetter(pth)
    pth = _convertUnixSlashes(pth)
    pth = _unescapeUnix(pth)
    _setClipboardContent(pth)
    return pth


def _toUnix(pth):
    """Converts the given Windows path to Unix convention."""
    pth = _convertWindowsDriveLetter(pth)
    pth = _convertWindowsSlashes(pth)
    pth = _escapeWindows(pth)
    _setClipboardContent(pth)
    return pth


def sl(pth=None):
    """Fetches the pth and converts it to Unix convention."""
    pth = _ensurePath(pth)
    return _toUnix(pth)


def bsl(pth=None):
    """Fetches the pth and converts it to Windows convention."""
    pth = _ensurePath(pth)
    return _toWindows(pth)
