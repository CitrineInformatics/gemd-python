"""Utility functions."""
import uuid
from copy import deepcopy

from taurus.entity.base_entity import BaseEntity
from taurus.entity.dict_serializable import DictSerializable
from taurus.entity.link_by_uid import LinkByUID
from toolz import concatv


def set_uuids(obj, name="auto"):
    """
    Recursively assign a uuid to every BaseEntity that doesn't already contain a uuid.

    This ensures that all of the pointers in the object can be replaced with LinkByUID objects
    :param obj: to recursively assign uuids to
    :param name: of the uuid to assign (default: "auto")
    :return: None
    """
    def func(base_obj):
        if len(base_obj.uids) == 0:
            base_obj.add_uid(name, str(uuid.uuid4()))
        return
    recursive_foreach(obj, func)
    return


def substitute_links(obj, native_uid=None):
    """
    Recursively replace pointers to BaseEntity with LinkByUID objects.

    This prepares the object to be serialized or written to the API.
    It is the inverse of substitute_objects.
    It is an in-place operation.
    :param obj: target of the operation
    :param native_uid: preferred uid to use for creating LinkByUID objects (Default: None)
    :return: None
    """
    _recursive_substitute(obj, native_uid)
    return


def substitute_objects(obj, index):
    """
    Recursively replace LinkByUID objects with pointers to the objects with that UID in the index.

    This prepares the object to be used after being deserialized.
    It is the inverse of substitute_links.
    It is an in-place operation.
    :param obj: target of the operation
    :param index: containing the objects that the uids point to
    :return: None
    """
    visited = set()

    def substitute(thing):
        if id(thing) in visited:
            return
        visited.add(id(thing))
        if isinstance(thing, (list, tuple)):
            for i, x in enumerate(thing):
                if isinstance(x, LinkByUID) and (x.scope.lower(), x.id) in index:
                    thing[i] = index[(x.scope.lower(), x.id)]
                    substitute(thing[i])
                else:
                    substitute(x)
        elif isinstance(thing, dict):
            for k, v in thing.items():
                if isinstance(v, LinkByUID) and (v.scope.lower(), v.id) in index:
                    thing[k] = index[(v.scope.lower(), v.id)]
                    substitute(thing[k])
                else:
                    substitute(v)
            for k, v in thing.items():
                if isinstance(k, LinkByUID) and (k.scope.lower(), k.id) in index:
                    thing[index[(k.scope.lower(), k.id)]] = v
                    del thing[k]
                else:
                    substitute(k)
        elif isinstance(thing, DictSerializable):
            for k, v in vars(thing).items():
                if isinstance(thing, BaseEntity) and k in thing.skip:
                    continue
                if isinstance(v, LinkByUID) and (v.scope.lower(), v.id) in index:
                    # Use setattr() to call setter logic
                    setattr(thing, k.lstrip('_'), index[(v.scope.lower(), v.id)])
                    substitute(thing.__dict__[k])
                else:
                    substitute(v)
        return

    substitute(obj)
    return


def flatten(obj):
    """
    Flatten a BaseEntity into a list of objects connected by LinkByUID objects.

    This is a composite operation the amounts to:
      - Making sure at least one uid is set in each BaseEntity in scope
      - Getting a list of unique objects contained in the scope
      - Substituting the pointers in those objects with LinkByUID objects
    :param obj: defining the scope of the flatten
    :return: a list of BaseEntity with LinkByUIDs to any BaseEntity members
    """
    # The ids should be set in the actual object so they are consistent
    set_uuids(obj)

    # make a copy before we substitute the pointers for links
    copy = deepcopy(obj)

    # list of uids that we've seen, to avoid returning duplicates
    known_uids = set()

    def _flatten(base_obj):
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

    res = recursive_flatmap(copy, _flatten)
    [substitute_links(x) for x in res]
    return res


def recursive_foreach(obj, func, apply_first=False, seen=None):
    """
    Apply a function recursively to each BaseEntity object.

    :param obj: target of the operation
    :param func: to apply to each contained BaseEntity
    :param apply_first: whether to apply the func before applying it to members (default: false)
    :param seen: set of seen objects (default=None).  DON'T PASS THIS!!!
    :return: None
    """
    if seen is None:
        seen = set({})
    if obj.__hash__ is not None:
        if obj in seen:
            return
        else:
            seen.add(obj)

    if isinstance(obj, (list, tuple)):
        for i, x in enumerate(obj):
            if isinstance(x, BaseEntity):
                if apply_first:
                    func(x)
                    recursive_foreach(x, func, apply_first, seen)
                else:
                    recursive_foreach(x, func, apply_first, seen)
                    func(x)
            else:
                recursive_foreach(x, func, apply_first, seen)
    elif isinstance(obj, dict):
        for x in concatv(obj.keys(), obj.values()):
            if isinstance(x, BaseEntity):
                if apply_first:
                    func(x)
                    recursive_foreach(x, func, apply_first, seen)
                else:
                    recursive_foreach(x, func, apply_first, seen)
                    func(x)
            else:
                recursive_foreach(x, func, apply_first, seen)
    elif isinstance(obj, DictSerializable):
        for k, x in obj.__dict__.items():
            if isinstance(obj, BaseEntity) and k in obj.skip:
                continue
            if isinstance(x, BaseEntity):
                if apply_first:
                    func(x)
                    recursive_foreach(x, func, apply_first, seen)
                else:
                    recursive_foreach(x, func, apply_first, seen)
                    func(x)
            else:
                recursive_foreach(x, func, apply_first, seen)
    return


def recursive_flatmap(obj, func, seen=None):
    """
    Recursively apply and accumulate a list-valued function to BaseEntity members.

    :param obj: target of the operation
    :param func: function to apply; must be list-valued
    :param seen: set of seen objects (default=None).  DON'T PASS THIS
    :return: a list of accumulated return values
    """
    res = []

    if seen is None:
        seen = set({})
    if obj.__hash__ is not None:
        if obj in seen:
            return res
        else:
            seen.add(obj)

    if isinstance(obj, (list, tuple)):
        for i, x in enumerate(obj):
            if isinstance(x, BaseEntity):
                res.extend(recursive_flatmap(x, func, seen))
                res.extend(func(x))
            else:
                res.extend(recursive_flatmap(x, func, seen))
    elif isinstance(obj, dict):
        for x in concatv(obj.keys(), obj.values()):
            if isinstance(x, BaseEntity):
                res.extend(recursive_flatmap(x, func, seen))
                res.extend(func(x))
            else:
                res.extend(recursive_flatmap(x, func, seen))
    elif isinstance(obj, DictSerializable):
        for k, x in sorted(obj.__dict__.items()):
            if isinstance(obj, BaseEntity) and k in obj.skip:
                continue
            if isinstance(x, BaseEntity):
                res.extend(recursive_flatmap(x, func, seen))
                res.extend(func(x))
            else:
                res.extend(recursive_flatmap(x, func, seen))
    return res


def _recursive_substitute(obj, native_uid=None, seen=None):
    if seen is None:
        seen = set({})
    if obj.__hash__ is not None:
        if obj in seen:
            return
        else:
            seen.add(obj)

    if isinstance(obj, (list, tuple)):
        for i, x in enumerate(obj):
            if isinstance(x, BaseEntity):
                if len(x.uids) == 0:
                    raise ValueError("No UID for {}".format(x))
                elif native_uid and native_uid in x.uids:
                    obj[i] = LinkByUID(native_uid, x.uids[native_uid])
                else:
                    uid_to_use = next(iter(x.uids.items()))
                    obj[i] = LinkByUID(uid_to_use[0], uid_to_use[1])
            else:
                _recursive_substitute(x, native_uid, seen)
    elif isinstance(obj, dict):
        for k, x in obj.items():
            if isinstance(x, BaseEntity):
                if len(x.uids) == 0:
                    raise ValueError("No UID for {}".format(x))
                elif native_uid and native_uid in x.uids:
                    obj[k] = LinkByUID(native_uid, x.uids[native_uid])
                else:
                    uid_to_use = next(iter(x.uids.items()))
                    obj[k] = LinkByUID(uid_to_use[0], uid_to_use[1])
            else:
                _recursive_substitute(x, native_uid, seen)
        for k, x in obj.items():
            if isinstance(k, BaseEntity):
                if len(k.uids) == 0:
                    raise ValueError("No UID for {}".format(k))
                elif native_uid and native_uid in k.uids:
                    obj[LinkByUID(native_uid, k.uids[native_uid])] = x
                    del obj[k]
                else:
                    uid_to_use = next(iter(k.uids.items()))
                    obj[LinkByUID(uid_to_use[0], uid_to_use[1])] = x
                    del obj[k]
            else:
                _recursive_substitute(k, native_uid, seen)
    elif isinstance(obj, DictSerializable):
        for k, x in obj.__dict__.items():
            if isinstance(obj, BaseEntity) and k in obj.skip:
                continue
            if isinstance(x, BaseEntity):
                if len(x.uids) == 0:
                    raise ValueError("No UID for {}".format(x))
                elif native_uid and native_uid in x.uids:
                    obj.__dict__[k] = LinkByUID(native_uid, x.uids[native_uid])
                else:
                    uid_to_use = next(iter(x.uids.items()))
                    obj.__dict__[k] = LinkByUID(uid_to_use[0], uid_to_use[1])
            else:
                _recursive_substitute(x, native_uid, seen)
    return
