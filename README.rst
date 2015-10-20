slbsl
=====

Convert paths from Windows to UNIX and vice versa.

Written to slightly ease the pain of working in environments that use both like a bash on Windows. Do not pass arbitrary text to the tool, only a path (though it may be wrapped in quotation marks).


Installation
------------

    pip install slbsl


Dependencies
------------

`pyperclip <http://pypi.python.org/pypi/pyperclip>`_ for clipboard functionality.


Tests
-----

You need `pytest <http://pypi.python.org/pypi/pytest>`_ installed.

    py.test test_slbsl -v


Usage
-----

The package installs a few shell scripts that you can call::

     sl [path] : Converts <path> or clipboard content to UNIX convention.
    bsl [path] : Converts <path> or clipboard content to Windows convention.
    fsl [path] : Flips slashes in <path> or clipboard content to their opposite individually.

The result is returned to the commandline and stored additionally in the clipboard.


Why the stupid name?
--------------------

**sl** ash **b** ack **sl** ash