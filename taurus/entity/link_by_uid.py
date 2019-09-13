"""A unique id that stands in for a data object."""
import uuid

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

    @classmethod
    def from_entity(cls, entity, name="auto"):
        """Create LinkByUID from in-memory object using id with scope 'name'."""
        if name in entity.uids:
            scope, id = name, entity.uids[name]
        else:
            if not entity.uids:
                entity.add_uid(name, str(uuid.uuid4()))
            scope, id = next((s, i) for s, i in entity.uids.items())
        return LinkByUID(scope, id)
