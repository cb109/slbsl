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
    """Make sure our testcases are not empty."""
    assert len(testcases) == 10


@pytest.mark.parametrize("winpath,unixpath",
                         testcases().items())
def test_sl(winpath, unixpath):
    """Test conversion of Windows to Unix path conventions."""
    assert slbsl.sl(winpath) == unixpath


@pytest.mark.parametrize("winpath,unixpath",
                         testcases().items())
def test_bsl(winpath, unixpath):
    """Test conversion of Unix to Windows path conventions."""
    assert slbsl.bsl(unixpath) == winpath
