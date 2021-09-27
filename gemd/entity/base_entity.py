"""Base class for all entities."""
from gemd.entity.dict_serializable import DictSerializable
from gemd.entity.case_insensitive_dict import CaseInsensitiveDict


class BaseEntity(DictSerializable):
    """
    Base class for any entity, which includes objects and templates.

    Parameters
    ----------
    uids: Map[str, str]
        A collection of
        `unique IDs <https://citrineinformatics.github.io/gemd-documentation/
        specification/unique-identifiers/>`_.
    tags: List[str]
        `Tags <https://citrineinformatics.github.io/gemd-documentation/specification/tags/>`_
        are hierarchical strings that store information about an entity. They can be used
        for filtering and discoverability.

    """

    typ = "base"

    def __init__(self, uids, tags):
        self._tags = None
        self.tags = tags

        self._uids = None
        self.uids = uids

    @property
    def tags(self):
        """Get the tags."""
        return self._tags

    @tags.setter
    def tags(self, tags):
        if tags is None:
            self._tags = []
        elif isinstance(tags, list):
            self._tags = tags
        else:
            self._tags = [tags]

    @property
    def uids(self):
        """Get the uids."""
        return self._uids

    @uids.setter
    def uids(self, uids):
        if uids is None:
            self._uids = CaseInsensitiveDict()
        elif isinstance(uids, dict):
            self._uids = CaseInsensitiveDict(**uids)
        else:
            self._uids = CaseInsensitiveDict(**{uids[0]: uids[1]})

    def add_uid(self, scope, uid):
        """
        Add a uid.

        Parameters
        ----------
        scope: str
            scope of the uid
        uid: str
            Unique identifier

        """
        self.uids[scope] = uid

    # Note that this could violate transitivity -- Link(scope1) == obj == Link(scope2)
    def __eq__(self, other):
        from gemd.entity.link_by_uid import LinkByUID
        if isinstance(other, LinkByUID):
            return self.uids.get(other.scope) == other.id
        else:
            result = super().__eq__(other)
            return result

    # Note the hash function checks if objects are identical, as opposed to the equals method,
    # which checks if fields are equal.  This is because BaseEntities are fundamentally
    # mutable objects.
    def __hash__(self):
        return super().__hash__()
