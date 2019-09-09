"""Methods for setting and validating."""
from taurus.entity.valid_list import ValidList


def validate_list(obj, typ, trigger=None):
    """Attempts to return obj as a list, each element of which has type typ."""
    if obj is None:
        return ValidList([], typ, trigger)
    elif isinstance(obj, list):
        return ValidList(obj, typ, trigger)
    else:
        return ValidList([obj], typ, trigger)


def validate_str(obj):
    """Check that obj is a string and then convert it to unicode."""
    if not isinstance(obj, str):
        raise ValueError("Expected a string but got {} instead".format(type(obj)))

    # If python 2 and the string isn't already unicode, turn it into unicode"""
    try:
        return obj.decode("utf-8")
    except AttributeError:
        return obj
