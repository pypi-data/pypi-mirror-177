"""Tests for the some_tool module."""
import pytest

from .. import some_tool


def test_some_function_exceptions():
    """Tests for exceptions of some_function()"""
    with pytest.raises(some_tool.BadValue):
        some_tool.some_function("", "")

    with pytest.raises(some_tool.BadValue):
        some_tool.some_function("foo", "")


# fmt: off
@pytest.mark.parametrize("val1,val2,exp", [
    ("HELLO", "world", "helloWORLD"),
    ("hello", "WORLD", "helloWORLD"),
    ("Hello", "World", "helloWORLD"),
])
# fmt: on
def test_some_function(val1: str, val2: str, exp: str):
    """Tests for some_function()"""
    res = some_tool.some_function(val1, val2)
    assert res == exp
