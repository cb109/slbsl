import pytest

import slbsl


@pytest.fixture
def testcases():
    """Maps windows paths to their unix equivalents."""
    return {
        # Basic paths.
        "C:\\": r"/C/",
        r"C:\path\to\thing": r"/C/path/to/thing",

        # Whitespace and special characters.
        r"C:\Program Files (x86)\Autodesk\Backburner\docs": r"/C/Program\ Files\ \(x86\)/Autodesk/Backburner/docs",
        r"C:\Users\username\Google Drive\Sublime Text 2.0.2 Portable\SourceCodePro_FontsOnly-1.017\OTF": r"/C/Users/username/Google\ Drive/Sublime\ Text\ 2.0.2\ Portable/SourceCodePro_FontsOnly-1.017/OTF",

        # Wrapped in "" quotation marks.
        r'"C:\"': r'"/C/"',
        r'"""C:\"""': r'"""/C/"""',
        r'"C:\Program Files (x86)\Autodesk\Backburner\docs"': r'"/C/Program\ Files\ \(x86\)/Autodesk/Backburner/docs"',

        # Wrapped in '' quotation marks.
        r"'C:\'": r"'/C/'",
        r"'''C:\'''": r"'''/C/'''",
        r"'C:\Program Files (x86)\Autodesk\Backburner\docs'": r"'/C/Program\ Files\ \(x86\)/Autodesk/Backburner/docs'",
    }


def test_datavalid(testcases):
    assert len(testcases) == 10


def test_sl(testcases):
    for winpath, unixpath in testcases.items():
        assert slbsl.sl(winpath) == unixpath


def test_bsl(testcases):
    for winpath, unixpath in testcases.items():
        assert slbsl.bsl(unixpath) == winpath
