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
    def from_entity(cls, entity):
        """Creates link using in-memory object. Assigns an ID linked object doesn't have one already."""
        if 'id' in entity.uids:
            scope, id = 'id', entity.uids['id']
        else:
            if not entity.uids:
                entity.add_uid('auto', str(uuid.uuid4()))
            scope, id = next((s, i) for s, i in entity.uids.items())
        return LinkByUID(scope, id)
