from json import JSONEncoder
from uuid import UUID

from gemd.entity.dict_serializable import DictSerializable

__all__ = ["GEMDEncoder"]


class GEMDEncoder(JSONEncoder):
    """Rules for encoding gemd objects as json strings."""

    def default(self, o):
        """Default encoder implementation."""
        if isinstance(o, DictSerializable):
            return o.as_dict()
        elif isinstance(o, UUID):
            return str(o)
        else:
            return JSONEncoder.default(self, o)
