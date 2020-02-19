"""Taurus JSON support, which provides a drop-in replacement for json.

This module provides the four main python json methods:

* :func:`dump` for serializing python and taurus objects to a JSON file
* :func:`load` for deserializing python and taurus objects from a JSON file
* :func:`dumps` for serializing python and taurus objects into a String
* :func:`loads` for deserializing python and taurus objects from a String

These methods should provide drop-in support for serialization and deserialization of
taurus-containing data structures by replacing imports of ``json`` with those of ``taurus.json``.

It also provides convenience imports of :class:`~taurus_encoder.TaurusEncoder`
and :class:`~taurus_json.TaurusJson`.
These classes can be used by developers to integrate taurus with other tools by extending the
JSON support provided here to those tools.
"""

from .taurus_encoder import TaurusEncoder  # noqa: F401
from .taurus_json import TaurusJson

__default = TaurusJson()


def loads(json_str, **kwargs):
    """
    Deserialize a json-formatted string into a taurus object.

    Parameters
    ----------
    json_str: str
        A string representing the serialized objects, such as what is produced by :func:`dumps`.
    **kwargs: keyword args, optional
        Optional keyword arguments to pass to `json.loads()`.

    Returns
    -------
    DictSerializable or List[DictSerializable]
        Deserialized versions of the objects represented by `json_str`, with links turned
        back into python object references.

    """
    return __default.loads(json_str, **kwargs)


def dumps(obj, **kwargs):
    """
    Serialize a taurus object, or container of them, into a json-formatting string.

    Parameters
    ----------
    obj: DictSerializable or List[DictSerializable]
        The object(s) to serialize to a string.
    **kwargs: keyword args, optional
        Optional keyword arguments to pass to `json.dumps()`.

    Returns
    -------
    str
        A string version of the serialized objects.

    """
    return __default.dumps(obj, **kwargs)


def load(fp, **kwargs):
    """
    Load serialized string representation of an object from a file.

    Parameters
    ----------
    fp: file
        File to read.
    **kwargs: keyword args, optional
        Optional keyword arguments to pass to `json.loads()`.

    Returns
    -------
    DictSerializable or List[DictSerializable]
        Deserialized object(s).

    """
    return __default.load(fp, **kwargs)


def dump(obj, fp, **kwargs):
    """
    Dump an object to a file, as a serialized string.

    Parameters
    ----------
    obj: DictSerializable or List[DictSerializable]
        Object(s) to dump
    fp: file
        File to write to.
    **kwargs: keyword args, optional
        Optional keyword arguments to pass to `json.dumps()`.

    Returns
    -------
    None

    """
    return __default.dump(obj, fp, **kwargs)
