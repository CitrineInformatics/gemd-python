"""Custom exception hierarchy for gemd.

All exceptions inherit from both a gemd base class and the corresponding
Python built-in, so existing ``except ValueError`` code continues to work.
"""
from pint.errors import DimensionalityError, UndefinedUnitError

__all__ = [
    "GemdError",
    "GemdValueError",
    "GemdBoundsError",
    "GemdValidationError",
    "GemdEnumerationError",
    "GemdSerializationError",
    "GemdTypeError",
    "GemdUnitError",
    "GemdIncompatibleUnitsError",
    "GemdUndefinedUnitError",
    "GemdKeyError",
]


class GemdError(Exception):
    """Base exception for all gemd errors."""

    def __init__(self, message, *, context=None, guidance=None):
        self.context = context
        self.guidance = guidance
        super().__init__(message)


class GemdValueError(GemdError, ValueError):
    """A value is invalid in the gemd context."""

    def __init__(self, message, *, expected=None, received=None,
                 context=None, guidance=None):
        self.expected = expected
        self.received = received
        super().__init__(message, context=context, guidance=guidance)


class GemdBoundsError(GemdValueError):
    """A value is outside the permitted bounds."""

    def __init__(self, message, *, bounds=None, value=None,
                 context=None, guidance=None):
        self.bounds = bounds
        self.value = value
        super().__init__(
            message, expected=str(bounds), received=str(value),
            context=context, guidance=guidance
        )


class GemdValidationError(GemdValueError):
    """A value is inconsistent with its template or schema."""


class GemdEnumerationError(GemdValueError):
    """An invalid enumeration choice was provided."""


class GemdSerializationError(GemdValueError):
    """A serialization or deserialization error occurred."""


class GemdTypeError(GemdError, TypeError):
    """A wrong argument type was provided."""

    def __init__(self, message, *, expected_type=None,
                 received_type=None, context=None, guidance=None):
        self.expected_type = expected_type
        self.received_type = received_type
        super().__init__(message, context=context, guidance=guidance)


class GemdUnitError(GemdError):
    """Base for unit-related errors."""


class GemdIncompatibleUnitsError(GemdUnitError, DimensionalityError):
    """Units cannot be converted between each other."""

    def __init__(self, message, *, context=None, guidance=None):
        self.context = context
        self.guidance = guidance
        Exception.__init__(self, message)


class GemdUndefinedUnitError(GemdUnitError, UndefinedUnitError):
    """A unit string is not recognized."""

    def __init__(self, message, *, context=None, guidance=None):
        self.context = context
        self.guidance = guidance
        Exception.__init__(self, message)


class GemdKeyError(GemdError, KeyError):
    """A key conflict in a case-insensitive dictionary."""

    def __init__(self, message, *, context=None, guidance=None):
        self.context = context
        self.guidance = guidance
        Exception.__init__(self, message)
