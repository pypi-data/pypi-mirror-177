"""Some tool."""


class BadValue(Exception):
    """BadValue exception."""


def some_function(value1: str, value2: str):
    """Some function"""
    if not value1:
        raise BadValue("Bad value1")

    if not value2:
        raise BadValue("Bad value2")

    return value1.lower() + value2.upper()
