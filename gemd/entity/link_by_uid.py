"""A unique id that stands in for a data object."""
from typing import TypeVar
import uuid

from gemd.entity.dict_serializable import DictSerializable

__all__ = ["LinkByUID"]
BaseEntityType = TypeVar("BaseEntityType", bound="BaseEntity")  # noqa: F821


class LinkByUID(DictSerializable, typ="link_by_uid"):
    """
    Link object, which replaces pointers to other entities before serialization and writing.

    Parameters
    ----------
    scope: str
        The scope of the unique identifier. Scopes are case-insensitive.
    id: str
        The unique identifier.

    """

    def __init__(self, scope, id):
        # TODO: parse to make sure it's valid
        self.scope = scope
        self.id = id

    def __repr__(self):
        return str({"scope": self.scope, "id": self.id})

    @classmethod
    def from_entity(cls, entity: BaseEntityType, *, scope=None):
        """
        Create LinkByUID from in-memory object.

        - If there exists an id with scope (default 'auto'), the LinkByUID object will be built
          with that scope.
        - If there is no id with scope, an arbitrary scope-id pair will be chosen.
        - If the object has no uids, the object will be mutated to include a uid (UUID4) with the
          chosen scope and the LinkByUID object will be built with that scope and id.

        Parameters
        ----------
        entity: BaseEntity
            The entity to substitute with a LinkByUID
        scope: str, optional
            The desired scope of the id.

        Returns
        -------
        LinkByUID
            A link object that references `entity` through its scope and id.

        """
        if scope is None:
            scope = "auto"  # set default

        if scope in entity.uids:
            uid = entity.uids[scope]
        else:
            if not entity.uids:
                entity.add_uid(scope, str(uuid.uuid4()))
            scope, uid = next((s, i) for s, i in entity.uids.items())
        return LinkByUID(scope, uid)

    # Note that this could violate transitivity
    def __eq__(self, other):
        from gemd.entity.base_entity import BaseEntity
        if isinstance(other, BaseEntity):
            if self.scope in other.uids:
                return other.uids[self.scope] == self.id
            else:
                return False
        elif isinstance(other, tuple):  # Make them interchangeable in a dict
            return len(other) == 2 and (self.scope, self.id) == other
        else:
            return super().__eq__(other)

    def __hash__(self):
        return hash((self.scope, self.id))
