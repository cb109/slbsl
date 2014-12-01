slbsl
=====

A small utility to convert slashes/backslashes to ease the pain of working
in environments that use both (e.g. bash on Windows).

Installation
------------

    pip install slbsl


Dependencies
------------

    pyperclip, for clipboard functionality.


Usage
-----

The package installs two shell script that you can call:

    sl [<path>] : Converts all backslashes in <path> or the clipboard to slashes.
    bsl [<path>] : Converts all slashes in <path> or the clipboard to backslashes.

The result is stored in the clipboard.