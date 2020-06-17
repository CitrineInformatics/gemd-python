"""A unique id that stands in for a data object."""
import uuid

from gemd.entity.dict_serializable import DictSerializable


class LinkByUID(DictSerializable):
    """
    Link object, which replaces pointers to other entities before serialization and writing.

    Parameters
    ----------
    scope: str
        The scope of the unique identifier. Scopes are case-insensitive.
    id: str
        The unique identifier.

    """

    typ = "link_by_uid"

    def __init__(self, scope, id):
        # TODO: parse to make sure it's valid
        self.scope = scope
        self.id = id

    def __repr__(self):
        return str({"scope": self.scope, "id": self.id})

    @classmethod
    def from_entity(cls, entity, name="auto"):
        """
        Create LinkByUID from in-memory object using id with scope 'name'.

        Parameters
        ----------
        entity: BaseEntity
            The entity to substitute with a LinkByUID
        name: str, optional
            The scope of the id.

        Returns
        -------
        LinkByUID
            A link object that references `entity` through its scope and id.

        """
        if name in entity.uids:
            scope, uid = name, entity.uids[name]
        else:
            if not entity.uids:
                entity.add_uid(name, str(uuid.uuid4()))
            scope, uid = next((s, i) for s, i in entity.uids.items())
        return LinkByUID(scope, uid)
