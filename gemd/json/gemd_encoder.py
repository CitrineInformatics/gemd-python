from json import JSONEncoder

from gemd.entity.dict_serializable import DictSerializable
from gemd.enumeration.base_enumeration import BaseEnumeration


class GEMDEncoder(JSONEncoder):
    """Rules for encoding gemd objects as json strings."""

    def default(self, o):
        """Default encoder implementation."""
        if isinstance(o, DictSerializable):
            return o.as_dict()
        elif isinstance(o, BaseEnumeration):
            return o.value
        else:
            return JSONEncoder.default(self, o)
