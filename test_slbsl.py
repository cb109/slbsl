import pytest
import pyperclip

import slbsl


@pytest.fixture
def slbsl_testcases():
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


@pytest.fixture
def fsl_testcases():
    """Paths with a mix of slashes and backslashes."""
    return {
        r"/": "\\",
        r"\\fileshare\test/project\shot/scene": r"//fileshare/test\project/shot\scene",
        r"foo/test/bar": r"foo\test\bar",
        r"foo\\test/bar": r"foo//test\bar",
        r"C:\dev\test\/foo/bar/file.py": r"C:/dev/test/\foo\bar\file.py",
        r"C:\dev\test\/\foo/\\bar/file.py": r"C:/dev/test/\/foo\//bar\file.py",
    }


@pytest.fixture
def esl_testcases():
    """Paths with a mix of slashes and backslashes."""
    return {
        r"/": r"/",
        r"\\fileshare\test/project\shot/scene": r"\\fileshare\test\project\shot\scene",
        r"foo/test/bar": r"foo/test/bar",
        r"foo\\test/bar": r"foo\\test\bar",
        r"C:\dev\test\/foo/bar/file.py": r"C:\dev\test\\foo\bar\file.py",
        r"C:\dev\test\/\foo/\\bar/file.py": r"C:\dev\test\\\foo\\\bar\file.py",
    }


def test_datavalid(slbsl_testcases, fsl_testcases, esl_testcases):
    """Make sure our testcases are not empty."""
    assert len(slbsl_testcases) == 10
    assert len(fsl_testcases) == 6
    assert len(esl_testcases) == 6


@pytest.mark.parametrize("winpath, unixpath", slbsl_testcases().items())
def test_sl(winpath, unixpath):
    """Test conversion of Windows to Unix path conventions."""
    assert slbsl.sl(winpath) == unixpath
    assert pyperclip.paste() == unixpath


@pytest.mark.parametrize("winpath, unixpath", slbsl_testcases().items())
def test_bsl(winpath, unixpath):
    """Test conversion of Unix to Windows path conventions."""
    assert slbsl.bsl(unixpath) == winpath
    assert pyperclip.paste() == winpath


@pytest.mark.parametrize("original, flipped", fsl_testcases().items())
def test_fsl(original, flipped):
    """Test flipping all slashes/backslashes."""
    assert slbsl.fsl(original) == flipped
    assert pyperclip.paste() == flipped

    assert slbsl.fsl(flipped) == original
    assert pyperclip.paste() == original


@pytest.mark.parametrize("original, equalized", esl_testcases().items())
def test_esl(original, equalized):
    """Test flipping all slashes/backslashes."""
    assert slbsl.esl(original) == equalized
    assert pyperclip.paste() == equalized
