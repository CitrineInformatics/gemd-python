from json import JSONEncoder

from taurus.entity.dict_serializable import DictSerializable
from taurus.enumeration.base_enumeration import BaseEnumeration


class TaurusEncoder(JSONEncoder):
    """Rules for encoding taurus objects as json strings."""

    def default(self, o):
        """Default encoder implementation."""
        if isinstance(o, DictSerializable):
            return o.as_dict()
        elif isinstance(o, BaseEnumeration):
            return o.value
        else:
            return JSONEncoder.default(self, o)
