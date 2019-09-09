"""A unique id that stands in for a data object."""
from taurus.entity.dict_serializable import DictSerializable


class LinkByUID(DictSerializable):
    """Link object, which replaces pointers to other entities before serialization and writing."""

    typ = "link_by_uid"

    def __init__(self, scope, id):
        # parse to make sure its valid
        self.scope = scope
        self.id = id

    def __repr__(self):
        return str({"scope": self.scope, "uid": self.id})
