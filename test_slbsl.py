import pyperclip
import pytest
import slbsl

# Maps windows paths to their unix equivalents.
SLBSL_TESTCASES = {
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

# Paths with a mix of slashes and backslashes.
FSL_TESTCASES = {
    r"/": "\\",
    r"\\fileshare\test/project\shot/scene": r"//fileshare/test\project/shot\scene",
    r"foo/test/bar": r"foo\test\bar",
    r"foo\\test/bar": r"foo//test\bar",
    r"C:\dev\test\/foo/bar/file.py": r"C:/dev/test/\foo\bar\file.py",
    r"C:\dev\test\/\foo/\\bar/file.py": r"C:/dev/test/\/foo\//bar\file.py",
}

# Paths with a mix of slashes and backslashes.
ESL_TESTCASES = {
    r"/": r"/",
    r"\\fileshare\test/project\shot/scene": r"\\fileshare\test\project\shot\scene",
    r"foo/test/bar": r"foo/test/bar",
    r"foo\\test/bar": r"foo\\test\bar",
    r"C:\dev\test\/foo/bar/file.py": r"C:\dev\test\\foo\bar\file.py",
    r"C:\dev\test\/\foo/\\bar/file.py": r"C:\dev\test\\\foo\\\bar\file.py",
}


def test_datavalid():
    """Make sure our testcases are not empty."""
    assert len(SLBSL_TESTCASES) == 10
    assert len(FSL_TESTCASES) == 6
    assert len(ESL_TESTCASES) == 6


@pytest.mark.parametrize("winpath, unixpath", SLBSL_TESTCASES.items())
def test_sl(winpath, unixpath):
    """Test conversion of Windows to Unix path conventions."""
    assert slbsl.sl(winpath) == unixpath
    assert pyperclip.paste() == unixpath


@pytest.mark.parametrize("winpath, unixpath", SLBSL_TESTCASES.items())
def test_bsl(winpath, unixpath):
    """Test conversion of Unix to Windows path conventions."""
    assert slbsl.bsl(unixpath) == winpath
    assert pyperclip.paste() == winpath


@pytest.mark.parametrize("original, flipped", FSL_TESTCASES.items())
def test_fsl(original, flipped):
    """Test flipping all slashes/backslashes."""
    assert slbsl.fsl(original) == flipped
    assert pyperclip.paste() == flipped

    assert slbsl.fsl(flipped) == original
    assert pyperclip.paste() == original


@pytest.mark.parametrize("original, equalized", ESL_TESTCASES.items())
def test_esl(monkeypatch, original, equalized):
    """Test flipping all slashes/backslashes."""

    monkeypatch.setattr("slbsl._is_windows", lambda: True)

    assert slbsl.esl(original) == equalized
    assert pyperclip.paste() == equalized
