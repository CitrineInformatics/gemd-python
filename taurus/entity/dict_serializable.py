"""An object that can be serializaed as a dictionary."""
from abc import ABC
import json


class DictSerializable(ABC):
    """A base class for objects that can be represented as a dictionary and serialized."""

    typ = NotImplemented
    skip = set()

    @classmethod
    def from_dict(cls, d):
        """Reconstitute the object from a dictionary."""
        # noinspection PyArgumentList
        # DictSerializable's constructor is not intended for use,
        # but all of its children will use from_dict like this.
        return cls(**d)

    def as_dict(self):
        """Convert the object to a dictionary."""
        keys = {x.lstrip('_') for x in vars(self) if x not in self.skip}
        attributes = {k: self.__getattribute__(k) for k in keys}
        attributes["type"] = self.typ
        return attributes

    def dump(self):
        """
        Convert the object to a JSON dictionary, so that every entry is serialized.

        Uses the json encoder client, so objects with uids are converted to LinkByUID dictionaries.
        """
        from taurus.client.json_encoder import dumps
        return json.loads(dumps(self))[1]

    @staticmethod
    def build(d):
        """Build an object from a JSON dictionary."""
        from taurus.client.json_encoder import loads, dumps
        return loads(dumps(d))

    def __repr__(self):
        return str(self.as_dict())

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
