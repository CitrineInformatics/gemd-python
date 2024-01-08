"""Base class for all enumerations."""
from deprecation import deprecated
from enum import Enum
from typing import Optional, Type, Callable
from warnings import warn

__all__ = ["BaseEnumeration"]


class BaseEnumeration(str, Enum):
    """Enumeration class that can convert between enumerations and associated values.

    BaseEnumeration is a powerful support class for string enumerations.  It inherits
    from both str and Enum to enable a class with str capabilities but still a
    restricted data space.  All constructors are case-insensitive on input and a given
    enumeration can recognize multiple synonyms for input, though only one value will
    correspond to the value itself.  For example:

        >>> class Fruits(BaseEnumeration):
        ...     APPLE = "Apple"
        ...     AVOCADO = "Avocado", "Alligator Pear"

    will recognize ``"apple"``, ``"APPLE"`` and ``"  aPpLe  "`` as referring to Fruits.APPLE,
    and ``"avocado"`` and ``"alligator pear"`` as referring to Fruits.AVOCADO.  However,
    since str(Fruits.AVOCADO) is ``"Avocado"``, Fruits.AVOCADO != ``"Alligator Pear"``.

    """

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

        """
        if val is None:
            result = None
        else:
            result = next((x for x in cls if str.lower(val).strip() in x.matches), None)
        if exception and result is None:
            raise ValueError(f"{val} is not a valid {cls}; valid choices are {[x for x in cls]}")
        return result

    @classmethod
    @deprecated(deprecated_in="1.15.0",
                removed_in="2.0.0",
                details="Enumerations autocast to values now.")
    def get_value(cls, name: str) -> str:
        """
        Return a valid value associated with name.

        If name is equal to one of the enum members, or to the value
        associated with an enum member, then return the relevant value.
        """
        if name is None:
            return None
        return cls.from_str(name, exception=True).value

    @classmethod
    @deprecated(deprecated_in="1.15.0",
                removed_in="2.0.0",
                details="Use from_str for retrieving the correct Enum object.")
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

    @classmethod
    def _missing_(cls, value: object) -> Optional["BaseEnumeration"]:
        """Allow Class(value) to resolve synonyms."""
        if isinstance(value, str):
            return cls.from_str(value)
        else:
            return None


def migrated_enum(*,
                  old_value: str,
                  new_value: str,
                  deprecated_in: str,
                  removed_in: str) -> Callable[[Type], Type]:
    """
    Decorator for registering an enumerated value as migrated to a new symbol.

    Parameters
    ----------
    old_value: str
        A string containing the old symbol name.  Used for display only.
    new_value: str
        A string containing the new symbol name or the enumeration value.  Used
        to resolve the target value.
    deprecated_in: str
        The version of the library the enumerated value was migrated.
    removed_in: str
        The version of the library the old enumerated value will be removed in.

    """
    def decorator(cls) -> Type:
        print("Sear")

        class MixinMeta(type(cls)):
            """New derived metaclass for holding the deprecated symbol."""

            def __getitem__(cls, name):
                if name == old_value:
                    warn(
                        f"{old_value} is deprecated as of {deprecated_in} "
                        f"and will be removed in {removed_in}. "
                        f"{old_value} has been renamed to {cls(new_value).name}.",
                        DeprecationWarning
                    )
                    return cls(new_value)
                else:
                    return super().__getitem__(name)

        def accessor(self):
            """Subroutine that returns the new enumerated value."""
            return cls(new_value)

        accessor.__name__ = old_value  # So deprecated knows the correct target name
        deprecator = deprecated(deprecated_in=deprecated_in,
                                removed_in=removed_in,
                                details=f"{old_value} has been renamed to {cls(new_value).name}.",
                                )

        # Add the property to the metaclass, and then update cls' meta
        setattr(MixinMeta, old_value, property(deprecator(accessor)))
        cls.__class__ = MixinMeta

        return cls

    return decorator
