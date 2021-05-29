"""Utility functions."""
import uuid
from typing import Dict, Callable, Union, Type, Tuple, List

from gemd.entity.base_entity import BaseEntity
from gemd.entity.dict_serializable import DictSerializable
from gemd.entity.link_by_uid import LinkByUID
from toolz import concatv


def set_uuids(obj, scope):
    """
    Recursively assign a uuid to every BaseEntity that doesn't already contain a uuid.

    This ensures that all of the pointers in the object can be replaced with LinkByUID objects
    :param obj: to recursively assign uuids to
    :param scope: of the uuid to assign
    :return: None
    """
    def func(base_obj):
        if len(base_obj.uids) == 0:
            base_obj.add_uid(scope, str(uuid.uuid4()))
        return
    recursive_foreach(obj, func)
    return


def _cached_isinstance_generator(
        class_or_tuple: Union[Type, Tuple[Type]]) -> Callable[[object], bool]:
    """
    Generate a function that checks and caches an isinstance(obj, class_or_tuple) call.

    :param class_or_tuple:
    :return: function with signature function(obj), returning isinstance(obj, class_or_tuple)
    """
    cache = dict()

    def func(obj):
        obj_type = type(obj)
        if obj_type not in cache:
            cache[obj_type] = isinstance(obj, class_or_tuple)
        return cache[obj_type]

    return func


def _substitute(thing,
                sub: Callable[[object], object],
                applies: Callable[[object], bool],
                visited: Dict[object, object] = None) -> object:
    """
    Generic recursive substitute function.

    Generates a new instance of thing by traversing its contents recursively, substituting
    values for which the sub function applies.
    :param thing: The object to traverse with substitution.
    :param sub: Function which provides substitute for value, should not have side-effects.
    :param applies: Function which defines the domain for the sub function to be invoked.
    """
    if visited is None:
        visited = {}
    if thing.__hash__ is not None and thing in visited:
        return visited[thing]
    if applies(thing):
        replacement = sub(thing)
        if thing.__hash__ is not None:
            visited[thing] = replacement
        new = _substitute(replacement, sub, applies, visited)
    elif isinstance(thing, list):
        new = [_substitute(x, sub, applies, visited) for x in thing]
    elif isinstance(thing, tuple):
        new = tuple(_substitute(x, sub, applies, visited) for x in thing)
    elif isinstance(thing, dict):
        new = {_substitute(k, sub, applies, visited): _substitute(v, sub, applies, visited)
               for k, v in thing.items()}
    elif isinstance(thing, DictSerializable):
        new_attrs = {_substitute(k, sub, applies, visited): _substitute(v, sub, applies, visited)
                     for k, v in thing.as_dict().items()}
        new = thing.build(new_attrs)
    else:
        new = thing

    if thing.__hash__ is not None:
        visited[thing] = new
    if new.__hash__ is not None:
        visited[new] = new

    # assert type(thing) == type(new), "{} is not {}".format(type(thing), type(new))
    return new


def make_index(obj):
    """
    Generates an index that can be used for the substitute_objects method.

    This method builds a dictionary of GEMD objects found by recursively crawling the passed
    object, indexed by all scope:id tuples found in any of the objects.  The passed object can
    be a list, tuple, dictionary or GEMD object.

    :param obj: target container (dict, list, ..) from which to create an index of GEMD objects

    """
    def _make_index(_obj: BaseEntity):
        return (((scope, _obj.uids[scope]), _obj) for scope in _obj.uids)

    idx = {}
    for uid, target in recursive_flatmap(obj, _make_index):
        idx[uid] = target

    return idx


def substitute_links(obj, native_uid=None):
    """
    Recursively replace pointers to BaseEntity with LinkByUID objects.

    This prepares the object to be serialized or written to the API.
    It is the inverse of substitute_objects.
    :param obj: target of the operation
    :param native_uid: preferred uid to use for creating LinkByUID objects (Default: None)
    """
    def make_link(entity: BaseEntity):
        if len(entity.uids) == 0:
            raise ValueError("No UID for {}".format(entity))
        elif native_uid and native_uid in entity.uids:
            return LinkByUID(native_uid, entity.uids[native_uid])
        else:
            return LinkByUID.from_entity(entity)

    return _substitute(obj, sub=make_link,
                       applies=lambda o: o is not obj and isinstance(o, BaseEntity))


def substitute_objects(obj, index):
    """
    Recursively replace LinkByUID objects with pointers to the objects with that UID in the index.

    This prepares the object to be used after being deserialized.
    It is the inverse of substitute_links.
    :param obj: target of the operation
    :param index: containing the objects that the uids point to
    """
    return _substitute(obj,
                       sub=lambda l: index.get((l.scope.lower(), l.id), l),
                       applies=lambda o: isinstance(o, LinkByUID))


def flatten(obj, scope):
    """
    Flatten a BaseEntity into a list of objects connected by LinkByUID objects.

    This is a composite operation the amounts to:
      - Making sure at least one uid is set in each BaseEntity in scope
      - Getting a list of unique objects contained in the scope
      - Substituting the pointers in those objects with LinkByUID objects
      - Sorting the output so an object is listed after all of its dependencies

    Flattening obeys reverse chronological ordering: if you flatten a process, you _will_ get the
    ingredients of the process in the result, even though process.ingredients is skipped.
    This supports the flattening of entire material histories.

    :param obj: the object where the graph traversal starts
    :param scope: the scope of the autogenerated ids
    :return: a list of BaseEntity with LinkByUIDs to any BaseEntity members
    """
    # The ids should be set in the actual object so they are consistent
    set_uuids(obj, scope)

    # list of uids that we've seen, to avoid returning duplicates
    known_uids = set()

    def _flatten(base_obj):
        nonlocal known_uids
        to_return = []
        # get all the uids of this object
        uids = list(base_obj.uids.items())

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

    :param obj: target of the operation
    :param func: to apply to each contained BaseEntity
    :param apply_first: whether to apply the func before applying it to members (default: false)
    :return: None
    """
    seen = set()

    # The overhead for all the invocations of isinstance was substantial
    isinstance_base_entity = _cached_isinstance_generator(BaseEntity)
    isinstance_list_or_tuple = _cached_isinstance_generator((list, tuple))
    isinstance_dict = _cached_isinstance_generator(dict)
    isinstance_dict_serializable = _cached_isinstance_generator(DictSerializable)

    queue = [obj]
    while queue:
        this = queue.pop()
        if this.__hash__ is not None:
            if this in seen:
                continue
            else:
                seen.add(this)

        if apply_first and isinstance_base_entity(this):
            func(this)

        if isinstance_list_or_tuple(this):
            for x in this:
                queue.append(x)
        elif isinstance_dict(this):
            for x in concatv(this.keys(), this.values()):
                queue.append(x)
        elif isinstance_dict_serializable(this):
            for k, x in this.__dict__.items():
                queue.append(x)

        if not apply_first and isinstance_base_entity(this):
            func(this)

    return


def recursive_flatmap(obj:  Union[List, Tuple, Dict, BaseEntity, DictSerializable],
                      func: Callable[[BaseEntity], Union[List, Tuple]],
                      *,
                      unidirectional=True):
    """
    Recursively apply and accumulate a list-valued function to BaseEntity members.

    :param obj: target of the operation
    :param func: function to apply; must be list-valued
    :param unidirectional: only recurse through the writeable direction of bidirectional links
    :return: a list of accumulated return values
    """
    res = []
    seen = set()
    queue = [obj]

    # The overhead for all the invocations of isinstance was substantial
    isinstance_base_entity = _cached_isinstance_generator(BaseEntity)
    isinstance_list_or_tuple = _cached_isinstance_generator((list, tuple))
    isinstance_dict = _cached_isinstance_generator(dict)
    isinstance_dict_serializable = _cached_isinstance_generator(DictSerializable)

    while queue:
        this = queue.pop()

        if this.__hash__ is not None:
            if this in seen:
                continue
            else:
                seen.add(this)

        if isinstance_base_entity(this):
            res.extend(func(this))

        if isinstance_list_or_tuple(this):
            for x in this:
                queue.append(x)
        elif isinstance_dict(this):
            for x in concatv(this.keys(), this.values()):
                queue.append(x)
        elif isinstance_dict_serializable(this):
            for k, x in sorted(this.__dict__.items()):
                if unidirectional and isinstance_base_entity(this) and k in this.skip:
                    continue
                queue.append(x)

    return res


def writable_sort_order(key: Union[BaseEntity, str]) -> int:
    """Sort order for flattening such that the objects can be read back and re-nested."""
    from gemd.entity.object import MeasurementSpec, ProcessSpec, MaterialSpec, IngredientSpec, \
        MeasurementRun, IngredientRun, MaterialRun, ProcessRun
    from gemd.entity.template import ConditionTemplate, MaterialTemplate, MeasurementTemplate, \
        ParameterTemplate, ProcessTemplate, PropertyTemplate

    if isinstance(key, BaseEntity):
        typ = key.typ
    elif isinstance(key, str):
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
