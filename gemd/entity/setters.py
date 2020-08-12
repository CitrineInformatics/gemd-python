"""Methods for setting and validating."""
from gemd.entity.valid_list import ValidList


def validate_list(obj, typ, *, trigger=None):
    """
    Attempts to return obj as a list, each element of which has type typ.

    Parameters
    ----------
    obj: Any
        Object or list of objects, all of which should be of type typ.
    typ: Type
        The desired type of obj, or if obj is a list, every element of obj.
    trigger: function
        A function to invoke when putting obj into a list.

    Returns
    -------
    ValidList
        A list with all elements of obj.
        The list is constrained so that every element has type typ.

    """
    if obj is None:
        return ValidList([], typ, trigger)
    elif isinstance(obj, (list, tuple)):
        return ValidList(obj, typ, trigger)
    else:
        return ValidList([obj], typ, trigger)


def validate_str(obj):
    """
    Check that obj is a string and then convert it to unicode.

    Parameters
    ----------
    obj: Any
        Object that should be a string

    Returns
    -------
    str
        `obj` as a string.

    Raises
    -------
    ValueError
        If `obj` is not a string.

    """
    if not isinstance(obj, str):
        raise TypeError("Expected a string but got {} instead".format(type(obj)))

    # If python 2 and the string isn't already unicode, turn it into unicode"""
    try:
        return obj.decode("utf-8")
    except AttributeError:
        return obj
