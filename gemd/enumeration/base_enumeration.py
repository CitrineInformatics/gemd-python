"""Base class for all enumerations."""
from enum import Enum
from typing import Optional


class BaseEnumeration(str, Enum):
    """Enumeration class that can convert between enumerations and associated values."""

    def __new__(cls, value: str, *args):
        """Overloaded to allow for synonyms."""
        if any(not isinstance(x, str) for x in (value,) + args):
            raise ValueError("All values of enum {} must be strings".format(cls))
        if cls.from_str(value, exception=False) is not None:
            raise ValueError("Duplicates not allowed in enumerated set of values {}".format(cls))
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.synonyms = frozenset(args)
        obj.matches = frozenset([obj.lower()]).union(x.lower() for x in obj.synonyms)
        return obj

    @classmethod
    def from_str(cls, val: str, *, exception: bool = False) -> Optional["BaseEnumeration"]:
        """
        Given a string value, return the Enumeration object that matches.

        Parameters
        ----------
        val: str
            The string to match against.  Leading and trailing whitespace is ignored.
            Case is ignored.
        exception: bool
            Whether to raise an error if the string doesn't match anything.  Default: False.

        Returns
        -------
        BaseEnumeration
            The matching enumerated element, or None

        :param val:
        :param exception:
        :return:

        """
        if val is None:
            result = None
        else:
            result = next((x for x in cls if str.lower(val).strip() in x.matches), None)
        if exception and result is None:
            raise ValueError(f"{val} is not a valid {cls}; valid choices are {[x for x in cls]}")
        return result

    @classmethod
    def get_value(cls, name: str) -> "BaseEnumeration":
        """
        Return a valid value associated with name.

        If name is equal to one of the enum members, or to the value
        associated with an enum member, then return the relevant value.
        """
        if name is None:
            return None
        return cls.from_str(name, exception=True).value

    @classmethod
    def get_enum(cls, name: str) -> "BaseEnumeration":
        """
        Return the enumeration associated with name.

        If name is equal to one of the enum members, or to the value
        associated with an enum member, then return the relevant enumeration.
        """
        if name is None:
            return None
        return cls.from_str(name, exception=True)

    def __str__(self):
        """Return the value of the enumeration object."""
        return self.value
