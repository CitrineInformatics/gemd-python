import json
from typing import Dict, Any, Type

from gemd.entity.dict_serializable import DictSerializable
from gemd.entity.base_entity import BaseEntity
from gemd.entity.link_by_uid import LinkByUID
from gemd.json import GEMDEncoder
from gemd.util import flatten, substitute_links, set_uuids

__all__ = ["GEMDJson"]


class GEMDJson(object):
    """
    Class that provides json load/dump functionality that is compatible with gemd objects.

    The serialization and deserialization strategy implemented by this class is described in
    :ref:`Serialization In Depth`

    scope: defines the scope to use for autogenerated UUIDs for objects without uids
    """

    def __init__(self, scope: str = 'auto'):
        self._scope = scope
        self._clazz_index = dict()

    @property
    def scope(self) -> str:
        """Return the default scope value."""
        return self._scope

    def dumps(self, obj, **kwargs) -> str:
        """
        Serialize a gemd object, or container of them, into a json-formatting string.

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
        # create a top level list of [flattened_objects, link-i-fied return value]
        res = {"object": obj}

        additional = flatten(res, self.scope)
        res = substitute_links(res)
        res["context"] = additional
        return json.dumps(res, cls=GEMDEncoder, sort_keys=True, **kwargs)

    def loads(self, json_str: str, **kwargs):
        """
        Deserialize a json-formatted string into a gemd object.

        Parameters
        ----------
        json_str: str
            A string representing the serialized objects, like what is produced by :func:`dumps`.
        **kwargs: keyword args, optional
            Optional keyword arguments to pass to `json.loads()`.

        Returns
        -------
        DictSerializable or List[DictSerializable]
            Deserialized versions of the objects represented by `json_str`, with links turned
            back into pointers.

        """
        # Create an index to hold the objects by their uid reference
        # so we can replace links with pointers
        index = {}
        clazz_index = DictSerializable.class_mapping
        clazz_index.update(self._clazz_index)
        raw = json.loads(
            json_str,
            object_hook=lambda x: self._load_and_index(x,
                                                       index,
                                                       clazz_index=clazz_index,
                                                       substitute=True),
            **kwargs)
        # the return value is in the 2nd position.
        return raw["object"]

    def load(self, fp, **kwargs):
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
        return self.loads(fp.read(), **kwargs)

    def dump(self, obj, fp, **kwargs):
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
        fp.write(self.dumps(obj, **kwargs))
        return

    def copy(self, obj):
        """
        Copy an object by dumping and then loading it.

        Parameters
        ----------
        obj: DictSerializable
            Object to copy

        Returns
        -------
        DictSerializable
            A copy of `obj`.

        """
        return self.loads(self.dumps(obj))

    def raw_dumps(self, obj, **kwargs):
        """
        Serialize the object as-is, which could be as a nested object.

        Parameters
        ----------
        obj:
            Object to dump
        **kwargs: keyword args, optional
            Optional keyword arguments to pass to `json.dumps()`.

        Returns
        -------
        str
            A serialized string of `obj`, which could be nested

        """
        return json.dumps(obj, cls=GEMDEncoder, sort_keys=True, **kwargs)

    def thin_dumps(self, obj, **kwargs):
        """
        Serialize a "thin" version of an object in which pointers are replaced by links.

        Parameters
        ----------
        obj:
            Object to dump
        **kwargs: keyword args, optional
            Optional keyword arguments to pass to `json.dumps()`.

        Returns
        -------
        str
            A serialized string of `obj`, with link_by_uid in place of pointers to other objects.

        """
        set_uuids(obj, self.scope)
        res = substitute_links(obj)
        return json.dumps(res, cls=GEMDEncoder, sort_keys=True, **kwargs)

    def raw_loads(self, json_str, **kwargs):
        """
        Deserialize a json-formatted string with no context into a gemd object as-is.

        Parameters
        ----------
        json_str: str
            A string representing the serialized objects, like what is produced by :func:`dumps`.
        **kwargs: keyword args, optional
            Optional keyword arguments to pass to `json.loads()`.

        Returns
        -------
        DictSerializable or List[DictSerializable]
            Deserialized versions of the objects represented by `json_str`

        """
        # Create an index to hold the objects by their uid reference
        # so we can replace links with pointers
        index = {}
        clazz_index = DictSerializable.class_mapping
        clazz_index.update(self._clazz_index)
        return json.loads(
            json_str,
            object_hook=lambda x: self._load_and_index(x, index, clazz_index=clazz_index),
            **kwargs)

    @staticmethod
    def _load_and_index(
            d: Dict[str, Any],
            object_index: Dict[str, DictSerializable],
            clazz_index: Dict[str, Type],
            substitute: bool = False) -> DictSerializable:
        """
        Load the class based on the type string and index it, if a BaseEntity.

        This function is used as the object hook when deserializing gemd objects

        Parameters
        ----------
        d: dict
            dictionary to try to load into a registered class instance
        object_index: dict
            to add the object to if it is a BaseEntity
        substitute: bool
            whether to substitute LinkByUIDs when they are found in the index

        Returns
        -------
        object
            the deserialized object, or the input dict if it wasn't recognized

        """
        if "type" not in d:
            return d
        typ = d.pop("type")

        if typ not in clazz_index:
            raise TypeError("Unexpected base object type: {}".format(typ))

        clz = clazz_index[typ]
        obj = clz.from_dict(d)

        if isinstance(obj, BaseEntity):  # Add it to the object index
            for (scope, uid) in obj.uids.items():
                object_index[(scope.lower(), uid)] = obj

        if substitute and issubclass(clz, LinkByUID):  # sub it if possible
            if (obj.scope.lower(), obj.id) in object_index:
                obj = object_index[(obj.scope.lower(), obj.id)]

        return obj
