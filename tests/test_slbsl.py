import pytest

import pyperclip

import slbsl


@pytest.fixture
def testcases():
    """Maps windows paths to their unix equivalents."""
    return {
        r"C:\Program Files (x86)\Autodesk\Backburner\docs" : r"/C/Program\ Files\ \(x86\)/Autodesk/Backburner/docs",
        r"C:\Users\username\Google Drive\Sublime Text 2.0.2 Portable\SourceCodePro_FontsOnly-1.017\OTF" : r"/C/Users/username/Google\ Drive/Sublime\ Text\ 2.0.2\ Portable/SourceCodePro_FontsOnly-1.017/OTF"
    }


def test_datavalid(testcases):
    assert len(testcases) == 2


def test_sl(testcases):
    for winpath, unixpath in testcases.items():
        assert slbsl.sl(winpath) == unixpath


def test_bsl(testcases):
    for winpath, unixpath in testcases.items():
        assert slbsl.bsl(unixpath) == winpath
