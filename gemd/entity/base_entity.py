"""Base class for all entities."""
from typing import Optional, Union, Iterable, List, Set, FrozenSet, Mapping, Dict

from gemd.entity.dict_serializable import DictSerializable
from gemd.entity.has_dependencies import HasDependencies
from gemd.entity.case_insensitive_dict import CaseInsensitiveDict
from gemd.entity.setters import validate_list


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

    def __init__(self, uids: Mapping[str, str], tags: Iterable[str]):
        self._tags = None
        self.tags = tags

        self._uids = None
        self.uids = uids

    @property
    def tags(self) -> List[str]:
        """Get the tags."""
        return self._tags

    @tags.setter
    def tags(self, tags: Iterable[str]):
        self._tags = validate_list(tags, str)

    @property
    def uids(self) -> Mapping[str, str]:
        """Get the uids."""
        return self._uids

    @uids.setter
    def uids(self, uids: Mapping[str, str]):
        if uids is None:
            self._uids = CaseInsensitiveDict()
        elif isinstance(uids, Mapping):
            self._uids = CaseInsensitiveDict(**uids)
        else:
            self._uids = CaseInsensitiveDict(**{uids[0]: uids[1]})

    def add_uid(self, scope: str, uid: str):
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

    def to_link(self,
                scope: Optional[str] = None,
                *,
                allow_fallback: bool = False) -> 'LinkByUID':  # noqa: F821
        """
        Generate a LinkByUID for this object.

        Parameters
        ----------
        scope: str, optional
            scope of the uid to get
        allow_fallback: bool
            whether to grab another scope/id if chosen scope is missing (Default: False).

        Returns
        -------
        LinkByUID

        """
        from gemd.entity.link_by_uid import LinkByUID
        if len(self.uids) == 0:
            raise ValueError(f"{type(self)} {self.name} does not have any uids.")

        if (scope is None) or (allow_fallback and scope not in self.uids):
            scope = next(x for x in self.uids)

        uid = self.uids.get(scope, None)
        if uid is None:
            raise ValueError(f"{type(self)} {self.name} has no uid with scope {scope}.")

        return LinkByUID(scope=scope, id=uid)

    def all_dependencies(self) -> Set[Union["BaseEntity", "LinkByUID"]]:
        """Return a set of all immediate dependencies (no recursion)."""
        result = set()
        queue = [type(self)]
        while queue:
            cls = queue.pop()
            if issubclass(cls, HasDependencies) and \
                    "_local_dependencies" not in cls.__abstractmethods__:
                result |= cls._local_dependencies(self)
                queue.extend(cls.__bases__)
        return result

    @staticmethod
    def _cached_equals(this: 'BaseEntity',
                       that: 'BaseEntity',
                       *,
                       cache: Dict[FrozenSet, Optional[bool]] = None) -> Optional[bool]:
        """
        Compute and stash whether two Base Entities are equal in a recursive sense.

        The cache uses ternary logic to communicate state.  True or False indicate a completed
        evaluation.  If the cache contains None, this indicates that we have not yet completed
        an evaluation in an earlier frame of the stack.
        """
        if cache is None:
            cache = {}
        cache_key = frozenset((id(this), id(that)))
        if cache_key in cache:
            return cache[cache_key]
        cache[cache_key] = None  # Mark as in progress

        this_dict = this._dict_for_compare()
        that_dict = that._dict_for_compare()
        if this_dict.keys() != that_dict.keys():
            cache[cache_key] = False  # Mark as failed
            return False

        # Check UIDs for an easy potential win
        this_uids = this_dict.pop("uids")
        that_uids = that_dict.pop("uids")
        if this_uids != that_uids:
            cache[cache_key] = False  # Mark as failed
            return False

        # Crawl rest of values to verify they align
        for key in this_dict:
            this_value = this_dict[key]
            that_value = that_dict[key]
            if isinstance(this_value, BaseEntity) and isinstance(that_value, BaseEntity):
                if BaseEntity._cached_equals(this_value, that_value, cache=cache) is False:
                    cache[cache_key] = False  # Mark as failed
                    return False
            elif isinstance(this_value, Iterable) and isinstance(that_value, Iterable) \
                    and not isinstance(this_value, str) and not isinstance(that_value, str):
                # Necessary to maintain context for recursive parts of the structure
                this_list = list(this_value)
                that_list = list(that_value)
                if len(this_list) != len(that_list):
                    # If an object was flattened, certain lists may be empty
                    if len(this_list) == 0:
                        if len(this_uids) > 0:  # But if it was flattened, uids will save us
                            continue
                    if len(that_list) == 0:
                        if len(that_uids) > 0:  # But if it was flattened, uids will save us
                            continue
                    cache[cache_key] = False  # Mark as failed
                    return False

                # Finally crawl and compare
                for x in this_list:
                    found = False
                    i_found = None
                    if isinstance(x, BaseEntity):
                        for i_found, y in enumerate(that_list):
                            # Unless something really broke, y is a BaseEntity
                            result = BaseEntity._cached_equals(x, y, cache=cache)
                            if result is True:
                                found = True
                                break
                            elif result is None:
                                # Don't know yet; pass as False will appear elsewhere
                                found = None
                    else:
                        found = x in that_list
                    if found is True:
                        if i_found is not None:
                            del that_list[i_found]
                    elif found is False:
                        cache[cache_key] = False  # Mark as failed
                        return False

            elif this_value != that_value:  # __eq__ should be cheap
                cache[cache_key] = False  # Mark as failed
                return False

        cache[cache_key] = True  # All tests passed
        return True

    # Note that this could violate transitivity -- Link(scope1) == obj == Link(scope2)
    def __eq__(self, other):
        from gemd.entity.link_by_uid import LinkByUID
        if isinstance(other, LinkByUID):
            return self.uids.get(other.scope) == other.id
        elif isinstance(other, tuple):
            return len(other) == 2 and other[0] in self.uids and self.uids[other[0]] == other[1]
        elif isinstance(other, BaseEntity):
            # We have to be a little clever for efficiency and to avoid infinite recursion
            return BaseEntity._cached_equals(self, other)
        else:
            return super().__eq__(other)

    # Note the hash function checks if objects are identical, as opposed to the equals method,
    # which checks if fields are equal.  This is because BaseEntities are fundamentally
    # mutable objects.  Note that if you define an __eq__ method without defining a __hash__
    # method, the object will become unhashable.
    # https://docs.python.org/3/reference/datamodel.html#object.__hash
    def __hash__(self):
        return super().__hash__()
