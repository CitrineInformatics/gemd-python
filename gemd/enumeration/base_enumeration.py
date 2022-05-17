"""Base class for all enumerations."""
from enum import Enum


class BaseEnumeration(Enum):
    """Enumeration class that can convert between enumerations and associated values."""

    def __init__(self, *_):
        """Ensure that there are no duplicates in the enumeration."""
        cls = self.__class__
        if any(self.value == e.value for e in cls):
            raise ValueError("Duplicates not allowed in enumerated set of values {}".format(cls))
        if not isinstance(self.value, str):
            raise ValueError("All values of enum {} must be strings".format(cls))

    @classmethod
    def get_value(cls, name):
        """
        Return a valid value associated with name.

        If name is equal to one of the enum members, or to the value
        associated with an enum member, then return the relevant value.
        """
        if name is None:
            return None
        if any(name == e.value for e in cls):
            return name
        if any(name == e for e in cls):
            return name.value
        raise ValueError("'{}' is not a valid choice for enumeration {}".format(name, cls))

    @classmethod
    def get_enum(cls, name):
        """
        Return the enumeration associated with name.

        If name is equal to one of the enum members, or to the value
        associated with an enum member, then return the relevant enumeration.
        """
        if name is None:
            return None
        if any(name == e.value for e in cls):
            return next(e for e in cls if e.value == name)
        if any(name == e for e in cls):
            return name
        raise ValueError("'{}' is not a valid choice for enumeration {}".format(name, cls))
