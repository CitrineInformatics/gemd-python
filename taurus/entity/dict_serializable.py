from abc import ABC
import json
from copy import deepcopy


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
        # noinspection PyArgumentList
        # DictSerializable's constructor is not intended for use,
        # but all of its children will use from_dict like this.
        return cls(**d)

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
        from taurus.client.json_encoder import dumps
        return json.loads(dumps(self))[1]

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
        from taurus.client.json_encoder import loads, dumps
        return loads(dumps(d))

    def __repr__(self):
        from taurus.util.impl import substitute_links, set_uuids
        object_dict = self.as_dict()
        # as_dict skips over keys in `skip`, but they should be in the representation.
        skipped_keys = {x.lstrip('_') for x in vars(self) if x in self.skip}
        for key in skipped_keys:
            skipped_attribute = deepcopy(self.__getattribute__(key))
            # Replace links in skipped keys with LinkByUID to prevent infinite recursion loop.
            set_uuids(skipped_attribute)
            substitute_links(skipped_attribute)
            object_dict[key] = skipped_attribute
        return object_dict.__str__()

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
