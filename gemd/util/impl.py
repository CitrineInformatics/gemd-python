"""Utility functions."""
import uuid
import functools
from inspect import getmembers
from typing import Dict, Callable, Union, Type, Tuple, List, Any, Optional
from warnings import warn

from gemd.entity.base_entity import BaseEntity
from gemd.entity.dict_serializable import DictSerializable
from gemd.entity.link_by_uid import LinkByUID

from collections.abc import Reversible, Iterable, ByteString
from toolz import concatv


def set_uuids(obj, scope):
    """
    Recursively assign a uuid to every BaseEntity that doesn't already contain a uuid.

    This ensures that all of the pointers in the object can be replaced with LinkByUID objects

    Parameters
    ----------
    obj: BaseEntity
        object to recursively assign uuids to
    scope: str
        scope of the uuid to assign

    Returns
    -------
    None

    """
    def func(base_obj):
        if len(base_obj.uids) == 0:
            base_obj.add_uid(scope, str(uuid.uuid4()))
        return
    recursive_foreach(obj, func)
    return


def _cached_isinstance(
        obj: object,
        class_or_tuple: Union[Type, Tuple[Union[Type, Tuple[Type]]]]) -> bool:
    """
    Emulate isinstance builtin to take advantage of functools caching.

    Parameters
    ----------
    obj: object

    class_or_tuple: Union[Type, Tuple[Union[Type, Tuple[Type]]]]
        A single type, a tuple of types (potentially nested)

    Returns
    -------
    bool
        Whether an object is an instance of a class or of a subclass thereof.

    """
    obj_type = type(obj)
    return _cached_issubclass(obj_type, class_or_tuple)


@functools.lru_cache(maxsize=None)
def _cached_issubclass(
        cls: Type,
        class_or_tuple: Union[Type, Tuple[Union[Type, Tuple[Type]]]]) -> bool:
    """
    Emulate issubclass builtin to take advantage of functools caching.

    Parameters
    ----------
    obj: object

    class_or_tuple: Union[Type, Tuple[Union[Type, Tuple[Type]]]]
        A single type, a tuple of types (potentially nested)

    Returns
    -------
    bool
        Whether 'cls' is a derived from another class or is the same class.

    """
    return issubclass(cls, class_or_tuple)


def _substitute(thing: Any,
                sub: Callable[[object], object],
                applies: Callable[[object], bool],
                visited: Dict[object, object] = None) -> object:
    """
    Generic recursive substitute function.

    Generates a new instance of thing by traversing its contents recursively, substituting
    values for which the sub function applies.

    Parameters
    ----------
    thing: Any
        The object to traverse with substitution.
    sub: Callable[[object], object]
        Function which provides substitute for value; should not have side-effects.
    applies: Callable[[object], bool]
        Function which defines the domain for the sub function to be invoked.

    """
    if visited is None:
        visited = {}
    if thing.__hash__ is not None and thing in visited:
        return visited[thing]

    if applies(thing):
        replacement = sub(thing)
        if thing.__hash__ is not None:
            visited[thing] = replacement
    else:
        replacement = thing

    if _cached_isinstance(replacement, list):
        new = [_substitute(x, sub, applies, visited) for x in replacement]
    elif _cached_isinstance(replacement, tuple):
        new = tuple(_substitute(x, sub, applies, visited) for x in replacement)
    elif _cached_isinstance(replacement, dict):
        new = {_substitute(k, sub, applies, visited): _substitute(v, sub, applies, visited)
               for k, v in replacement.items()}
    elif _cached_isinstance(replacement, DictSerializable):
        new_attrs = {_substitute(k, sub, applies, visited): _substitute(v, sub, applies, visited)
                     for k, v in replacement.as_dict().items()}
        new = replacement.build(new_attrs)
    else:
        new = replacement

    if thing.__hash__ is not None:
        visited[thing] = new

    return new


def _substitute_inplace(thing: Any,
                        sub: Callable[[object], object],
                        applies: Callable[[object], bool],
                        visited: Dict[object, object] = None) -> object:
    """
    Generic recursive in-place substitute function.

    Iteratively crawls the passed structure, substituting elements with sub(element) when
    applies(element) is true and the element is mutable.

    Parameters
    ----------
    thing: Any
        The object to traverse with substitution.
    sub: Callable[[object], object]
        Function which provides substitute for value; should not have side-effects.
    applies: Callable[[object], bool]
        Function which defines the domain for the sub function to be invoked.

    """
    def _key(obj):
        if obj.__hash__ is not None:
            return obj
        else:
            return id(obj)

    orig_key = _key(thing)
    if visited is None:
        visited = {}
    if orig_key in visited:
        return visited[orig_key]

    if applies(thing):
        thing = sub(thing)
    visited[orig_key] = thing  # Store before we start recursing

    if _cached_isinstance(thing, list):  # Change list in place
        for i, x in enumerate(thing):
            thing[i] = _substitute_inplace(x, sub, applies, visited)
    elif _cached_isinstance(thing, tuple):  # Tuples are immutable; regenerate
        thing = tuple(_substitute_inplace(x, sub, applies, visited) for x in thing)
        visited[orig_key] = thing  # We mutated it
    elif _cached_isinstance(thing, dict):  # Change dict in place, both keys & values
        remove = set()  # Store todos because can't mutate a dict in a loop
        update = dict()
        for k, v in thing.items():
            new_k = _substitute_inplace(k, sub, applies, visited)
            new_v = _substitute_inplace(v, sub, applies, visited)
            if id(k) != id(new_k):
                remove.add(k)
                update[new_k] = v
            if id(v) != id(new_v):
                update[new_k] = new_v
        for k in remove:
            thing.pop(k, None)
        thing.update(update)
    elif _cached_isinstance(thing, DictSerializable):
        for k, v in thing.as_dict().items():  # Assume key can't change b/c it's an attribute
            new_v = _substitute_inplace(v, sub, applies, visited)
            if id(v) != id(new_v):
                _setter_by_name(type(thing), k)(thing, new_v)

    return thing


@functools.lru_cache(maxsize=None)
def _setter_by_name(clazz: type, name: str) -> Callable:
    """Internal method to get the setter method for an attribute."""
    from gemd.entity.object import IngredientRun

    def _emulator(inner_name: str) -> Callable:
        return lambda self, value: setattr(self, inner_name, value)

    prop = next((x[1] for x in getmembers(clazz) if x[0] == name), None)
    if name == "name" and issubclass(clazz, IngredientRun):  # Weird exceptional case
        setter = _emulator(f"_name")
    elif prop is None:  # It's not a property, just an ordinary attribute
        setter = _emulator(name)
    else:
        setter = prop.fset

    return setter


def make_index(obj: Union[List, Tuple, Dict, BaseEntity, DictSerializable]):
    """
    Generates an index that can be used for the substitute_objects method.

    This method builds a dictionary of GEMD objects found by recursively crawling the passed
    object, indexed by all scope:id tuples found in any of the objects.  The passed object can
    be a list, tuple, dictionary or GEMD object.

    Parameters
    ----------
    obj: Union[List, Tuple, Dict, BaseEntity, DictSerializable]
        target container (dict, list, ..) from which to create an index of GEMD objects

    """
    def _make_index(_obj: BaseEntity):
        return ((LinkByUID(scope=scope, id=_obj.uids[scope]), _obj) for scope in _obj.uids)

    idx = {}
    for uid, target in recursive_flatmap(obj, _make_index):
        idx[uid] = target

    return idx


def substitute_links(obj: Any,
                     scope: Optional[str] = None,
                     *,
                     native_uid: str = None,
                     allow_fallback: bool = True,
                     inplace: bool = False
                     ):
    """
    Recursively replace pointers to BaseEntity with LinkByUID objects.

    This prepares the object to be serialized or written to the API.
    It is the inverse of substitute_objects.

    Parameters
    ----------
    obj: Any
        target of the operation
    scope: Optional[str], optional
        preferred scope to use for creating LinkByUID objects (Default: None)
    native_uid: str, optional
        DEPRECATED; former name for scope argument
    allow_fallback: bool, optional
        whether to grab another scope/id if chosen scope is missing (Default: True).
    inplace: bool, optional
        whether to replace objects in place, as opposed to returning a copy (Default: False).

    """
    if native_uid is not None:
        warn("The keyword argument 'native_uid' is deprecated.  When selecting a default scope, "
             "use the 'scope' keyword argument.", DeprecationWarning)
        if scope is not None:
            raise ValueError("Both 'scope' and 'native_uid' keywords passed.")
        scope = native_uid

    if inplace:
        method = _substitute_inplace
    else:
        method = _substitute

    return method(obj,
                  sub=lambda o: o.to_link(scope=scope, allow_fallback=allow_fallback),
                  applies=lambda o: o is not obj and _cached_isinstance(o, BaseEntity))


def substitute_objects(obj,
                       index,
                       *,
                       inplace: bool = False):
    """
    Recursively replace LinkByUID objects with pointers to the objects with that UID in the index.

    This prepares the object to be used after being deserialized.
    It is the inverse of substitute_links.

    Parameters
    ----------
    obj: Any
        target of the operation
    index: Dict[Tuple[str, str], BaseEntity]
        containing the objects that the uids point to
    inplace: bool, optional
        whether to replace objects in place, as opposed to returning a copy (Default: False).

    """
    if inplace:
        method = _substitute_inplace
    else:
        method = _substitute

    return method(obj,
                  sub=lambda l: index.get(l, l),
                  applies=lambda o: _cached_isinstance(o, LinkByUID))


def flatten(obj, scope=None):
    """
    Flatten a BaseEntity (or array of them) into a list of objects connected by LinkByUID objects.

    This is a composite operation the amounts to:
      - Making sure at least one uid is set in each BaseEntity in scope
      - Getting a list of unique objects contained in the scope
      - Substituting the pointers in those objects with LinkByUID objects
      - Sorting the output so an object is listed after all of its dependencies

    Flattening obeys reverse chronological ordering: if you flatten a process, you _will_ get the
    ingredients of the process in the result, even though process.ingredients is skipped.
    This supports the flattening of entire material histories.

    Parameters
    ----------
    obj: Any
        the object where the graph traversal starts
    scope: str, optional
        the scope of the autogenerated ids.
        If omitted, encountering a BaseEntity without an UIDs is fatal.

    Returns
    -------
    List[BaseEntity]
        a list of BaseEntity with LinkByUIDs to any BaseEntity members

    """
    # The ids should be set in the actual object so they are consistent
    if scope is not None:
        set_uuids(obj, scope)

    # list of uids that we've seen, to avoid returning duplicates
    known_uids = set()

    def _flatten(base_obj: BaseEntity):
        nonlocal known_uids
        to_return = []
        # get all the uids of this object
        uids = list(base_obj.uids.items())
        if len(uids) == 0:
            raise ValueError(f"No UID for {base_obj}; pass `flatten` a `scope` to set one")

        # if none of the uids are known, then its a new object and we should return it
        if not any(uid in known_uids for uid in uids):
            to_return = [base_obj]

        # add all of the uids of this object into the known uid list
        for uid in uids:
            known_uids.add(uid)

        return to_return

    res = recursive_flatmap(obj, _flatten, unidirectional=False)
    return sorted([substitute_links(x) for x in res], key=lambda x: writable_sort_order(x))


def recursive_foreach(obj: Union[List, Tuple, Dict, BaseEntity, DictSerializable],
                      func: Callable[[BaseEntity], None],
                      *,
                      apply_first=False):
    """
    Apply a function recursively to each BaseEntity object.

    Only objects of type BaseEntity will have the function applied, but the recursion will walk
    through all objects.  For example, BaseEntity -> list -> BaseEntity will have func applied
    to both base entities.

    Parameters
    ----------
    obj: Union[List, Tuple, Dict, BaseEntity, DictSerializable]
        target of the operation
    func: Callable[[BaseEntity], None]
        to apply to each contained BaseEntity
    apply_first: bool
        whether to apply the func before applying it to members (default: false)

    Returns
    -------
    None

    """
    seen = set()
    queue = [obj]

    while queue:
        this = queue.pop()
        if this.__hash__ is not None:
            if this in seen:
                continue
            else:
                seen.add(this)

        if apply_first and _cached_isinstance(this, BaseEntity):
            func(this)

        if _cached_isinstance(this, dict):
            for x in concatv(this.keys(), this.values()):
                queue.append(x)
        elif _cached_isinstance(this, DictSerializable):
            for k, x in this.__dict__.items():
                queue.append(x)
        elif _cached_isinstance(this, Iterable) \
                and not _cached_isinstance(this, (str, ByteString)):
            for x in this:
                queue.append(x)

        if not apply_first and _cached_isinstance(this, BaseEntity):
            func(this)

    return


def recursive_flatmap(obj: Union[List, Tuple, Dict, BaseEntity, DictSerializable],
                      func: Callable[[BaseEntity], Union[List, Tuple]],
                      *,
                      unidirectional=True):
    """
    Recursively apply and accumulate a list-valued function to BaseEntity members.

    Parameters
    ----------
    obj: Union[List, Tuple, Dict, BaseEntity, DictSerializable]
        target of the operation
    func: Callable[[BaseEntity], Union[List[Any], Tuple[Any]]]
        function to apply; must be list-valued
    unidirectional: bool
        only recurse through the writeable direction of bidirectional links

    Returns
    --------
    List[Any]
        a list of accumulated return values

    """
    res = []
    seen = set()
    queue = [obj]

    while queue:
        this = queue.pop()

        if this.__hash__ is not None:
            if this in seen:
                continue
            else:
                seen.add(this)

        if _cached_isinstance(this, BaseEntity):
            res.extend(func(this))

        if _cached_isinstance(this, dict):
            queue.extend(concatv(this.keys(), this.values()))
        elif _cached_isinstance(this, DictSerializable):
            for k, x in sorted(this.__dict__.items()):
                if unidirectional and _cached_isinstance(this, BaseEntity) and k in this.skip:
                    continue
                queue.append(x)
        elif _cached_isinstance(this, Reversible):
            queue.extend(reversed(this))  # Preserve order of the list/tuple
        elif _cached_isinstance(this, Iterable) \
                and not _cached_isinstance(this, (str, ByteString)):
            queue.extend(this)  # No control over order

    return res


def writable_sort_order(key: Union[BaseEntity, str]) -> int:
    """Sort order for flattening such that the objects can be read back and re-nested."""
    from gemd.entity.object import MeasurementSpec, ProcessSpec, MaterialSpec, IngredientSpec, \
        MeasurementRun, IngredientRun, MaterialRun, ProcessRun
    from gemd.entity.template import ConditionTemplate, MaterialTemplate, MeasurementTemplate, \
        ParameterTemplate, ProcessTemplate, PropertyTemplate

    if _cached_isinstance(key, BaseEntity):
        typ = key.typ
    elif _cached_isinstance(key, str):
        typ = key
    else:
        raise ValueError("Can ony sort BaseEntities and type strings, not {}".format(key))

    if typ in [ConditionTemplate.typ, ParameterTemplate.typ, PropertyTemplate.typ]:
        return 0
    if typ in [MaterialTemplate.typ, ProcessTemplate.typ, MeasurementTemplate.typ]:
        return 1
    if typ in [ProcessSpec.typ, MeasurementSpec.typ]:
        return 2
    if typ in [ProcessRun.typ, MaterialSpec.typ]:
        return 3
    if typ in [IngredientSpec.typ, MaterialRun.typ]:
        return 4
    if typ in [IngredientRun.typ, MeasurementRun.typ]:
        return 5

    raise ValueError("Unrecognized type string: {}".format(typ))
