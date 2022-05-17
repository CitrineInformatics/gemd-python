"""Methods for setting and validating."""
from gemd.entity.valid_list import ValidList

from typing import Union, Iterable, Optional, Callable, Type, TypeVar

T = TypeVar('T')


def validate_list(obj: Union[Iterable[T], T],
                  typ: Union[Iterable[Type], Type],
                  *,
                  trigger: Callable[[T], Optional[T]] = None) -> ValidList:
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
    elif isinstance(obj, Iterable) and not isinstance(obj, str):
        return ValidList(obj, typ, trigger)
    else:
        return ValidList([obj], typ, trigger)


def validate_str(obj) -> str:
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
    return obj
