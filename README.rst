slbsl
=====

Convert paths from Windows to UNIX and vice versa.

Written to slightly ease the pain of working in environments that use
both like a bash on Windows.


Installation
------------

    pip install slbsl


Dependencies
------------

`pyperclip <http://pypi.python.org/pypi/pyperclip>`_ for clipboard functionality.


Tests
-----

You need `pytest <http://pypi.python.org/pypi/pytest>`_ installed.

    py.test tests -v


Usage
-----

The package installs two shell script that you can call::

     sl [path] : Converts <path> or clipboard content to UNIX convention.
    bsl [path] : Converts <path> or clipboard content to Windows convention.

The result is returned to the commandline and stored additionally in the clipboard.


Why the stupid name?
--------------------

**sl** = slash, **bsl** = backslash