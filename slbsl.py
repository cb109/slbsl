"""
Convert paths from Windows to UNIX and vice versa.

This affects slashes vs backslashes, drive letters and escaping of
spaces and parentheses. Please note that the script is pretty dumb, so
make sure to give it a path, not arbitrary text.

If no text is given to the functions (or shell scripts), they will take
the clipboard content as input. The result is returned to the commandline
and also stored to the clipboard.

"""
import os
import re
import sys

import pyperclip

__all__ = ["sl", "bsl", "fsl", "esl"]


colon = ":"
slash = "/"
backslash = "\\"
space = " "
openpar = "("
closepar = ")"


def _get_commandline_input():
    """Returns commandline args as space-separated string."""
    args = sys.argv[1:]
    txt = " ".join(args) if args else None
    return txt


def _get_clipboard_content():
    """Returns the content of the Windows clipboard."""
    return str(pyperclip.paste())


def _set_clipboard_content(txt):
    """Sets the Windows clipboard content to the given text."""
    return pyperclip.copy(txt)


def _ensure_path(pth):
    """Tries to get pth either as given, or from commandline or the
    clipboard. If none of these source provide input, bail out."""
    pth = pth or _get_commandline_input() or _get_clipboard_content()
    if not pth:
        print(
            "ERROR - Could not get path from commandline "
            "or clipboard or it is empty."
        )
        sys.exit(1)
    return pth


def _convert_windows_drive_letter(pth):
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


def _escape_windows(pth):
    """Escapes certain characters in pth with a backslash."""
    for token in (space, openpar, closepar):
        pth = pth.replace(token, backslash + token)
    return pth


def _convert_windows_slashes(pth):
    """Replaces all backslashes in pth with slashes."""
    return pth.replace(backslash, slash)


def _convert_unix_drive_letter(pth):
    """Converts '/C/' to 'C:\'. Handles wrapping quotation marks."""
    starts_with_unix_driveletter = r"([\"\']*)(\/)(?P<drive>[a-zA-Z])(\/)"
    match = re.match(starts_with_unix_driveletter, pth)
    if match:
        drive = match.group("drive")
        drive_index = pth.find(drive)
        # Drop the leading slash, while keeping any quotation marks.
        pth = (
            pth[: drive_index - 1] + drive + colon + backslash + pth[drive_index + 2 :]
        )
    pth = pth.replace(colon + slash, colon + backslash)
    return pth


def _convert_unix_slashes(pth):
    """Replaces all slashes in pth with backslashes."""
    return pth.replace(slash, backslash)


def _unescape_unix(pth):
    """Removes backslashes in front of certain characters in pth."""
    for token in (space, openpar, closepar):
        pth = pth.replace(backslash + token, token)
    return pth


def _to_windows(pth):
    """Converts the given Unix path to Windows convention."""
    pth = _convert_unix_drive_letter(pth)
    pth = _convert_unix_slashes(pth)
    pth = _unescape_unix(pth)
    return pth


def _to_unix(pth):
    """Converts the given Windows path to Unix convention."""
    pth = _convert_windows_drive_letter(pth)
    pth = _convert_windows_slashes(pth)
    pth = _escape_windows(pth)
    return pth


def _flip(pth):
    """Flips each slash to a backslash and each backslash to a slash."""
    splash_tokens = pth.split(slash)
    splash_tokens = map(_convert_windows_slashes, splash_tokens)
    pth = backslash.join(splash_tokens)
    return pth


def _is_windows():
    return os.name == "nt"


def _equalize(pth):
    """Equalizes slashes in pth depending on whether slash or backslash
    is the majority.  In case of a draw, favor the one matching the os
    conventions."""
    num_slash = pth.count(slash)
    num_backslash = pth.count(backslash)
    if num_slash == num_backslash == 0:
        return pth
    elif num_slash > num_backslash:
        return _convert_windows_slashes(pth)
    elif num_backslash > num_slash:
        return _convert_unix_slashes(pth)
    else:  # Draw.
        if _is_windows():
            return _convert_unix_slashes(pth)
        else:
            return _convert_windows_slashes(pth)


def _pathcommand(func):
    """A decorator to make sure we fetch the pth from one of multiple
    sources, call the function and store the result to the clipboard."""

    def wrapper(pth=None):
        pth = _ensure_path(pth)
        pth = func(pth)
        _set_clipboard_content(pth)
        return pth

    return wrapper


@_pathcommand
def sl(pth=None):
    """Converts pth to Unix convention."""
    return _to_unix(pth)


@_pathcommand
def bsl(pth=None):
    """Converts pth to Windows convention."""
    return _to_windows(pth)


@_pathcommand
def fsl(pth=None):
    """Flips slashes in pth to their opposites."""
    return _flip(pth)


@_pathcommand
def esl(pth=None):
    """Equalize slashes in pth."""
    return _equalize(pth)
