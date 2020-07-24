from abc import ABC
from logging import getLogger

import json
import inspect

# There are some weird (probably resolvable) errors during object cloning if this is an
# instance variable of DictSerializable.
logger = getLogger(__name__)


class DictSerializable(ABC):
    """A base class for objects that can be represented as a dictionary and serialized."""

    typ = NotImplemented
    skip = set()

    @classmethod
    def from_dict(cls, d):
        """
        Reconstitute the object from a dictionary.

        Parameters
        ----------
        d: dict
            The object as a dictionary of key-value pairs that correspond to the object's fields.

        Returns
        -------
        DictSerializable
            The deserialized object.

        """
        expected_arg_names = inspect.getfullargspec(cls.__init__).args
        expected_arg_names += inspect.getfullargspec(cls.__init__).kwonlyargs
        kwargs = {}
        for name, arg in d.items():
            if name in expected_arg_names:
                kwargs[name] = arg
            elif name != 'type':
                logger.warning('Ignoring unexpected keyword argument in {}: {}'.format(
                    cls.__name__, name))
        # noinspection PyArgumentList
        # DictSerializable's constructor is not intended for use,
        # but all of its children will use from_dict like this.
        return cls(**kwargs)

    def as_dict(self):
        """
        Convert the object to a dictionary.

        Returns
        -------
        dict
            A dictionary representation of the object, where the keys are its fields.

        """
        keys = {x.lstrip('_') for x in vars(self) if x not in self.skip}
        attributes = {k: self.__getattribute__(k) for k in keys}
        attributes["type"] = self.typ
        return attributes

    def dump(self):
        """
        Convert the object to a JSON dictionary, so that every entry is serialized.

        Uses the json encoder client, so objects with uids are converted to LinkByUID dictionaries.

        Returns
        -------
        str
            A string representation of the object as a dictionary.

        """
        from gemd.json import GEMDJson
        encoder = GEMDJson()
        return json.loads(encoder.raw_dumps(self))

    @staticmethod
    def build(d):
        """
        Build an object from a JSON dictionary.

        This differs from `from_dict` in that the values themselves may *also* be dictionaries
        corresponding to serialized DictSerializable objects.

        Parameters
        ----------
        d: dict
            The object as a serialized dictionary.

        Returns
        -------
        DictSerializable
            The deserialized object.

        """
        from gemd.json import GEMDJson
        encoder = GEMDJson()
        return encoder.raw_loads(encoder.raw_dumps(d))

    def __repr__(self):
        object_dict = self.as_dict()
        # as_dict() skips over keys in `skip`, but they should be in the representation.
        skipped_keys = {x.lstrip('_') for x in vars(self) if x in self.skip}
        for key in skipped_keys:
            skipped_field = getattr(self, key, None)
            object_dict[key] = self._name_repr(skipped_field)
        return str(object_dict)

    def _name_repr(self, entity):
        """
        A representation of an object or a list of objects that uses the name and type.

        This is used to represent soft-linked objects without inundating the user with
        repetitive information.

        Parameters
        ----------
        entity: DictSerializable or List[DictSerializable]
            Object to represent using its name. Generally a (list of) BaseEntity or BaseAttribute,
            both of which have a `name` field.

        Returns
        -------
        str
            A representation of `entity` using its name.

        """
        if isinstance(entity, (list, tuple)):
            return [self._name_repr(item) for item in entity]
        elif entity is None:
            return None
        else:
            name = getattr(entity, 'name', '<unknown name>')
            return "<{} '{}'>".format(type(entity).__name__, name)

    def __eq__(self, other):
        if isinstance(other, DictSerializable):
            self_dict = self.as_dict()
            other_dict = other.as_dict()
            return self_dict == other_dict
        else:
            return False

    # TODO make a hash function which reflects __eq__?
    def __hash__(self):
        return super().__hash__()
