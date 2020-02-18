from .taurus_encoder import TaurusEncoder
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
        back into pointers.

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
