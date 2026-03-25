"""Tests for the custom exception hierarchy."""
import pytest

from gemd.exceptions import (
    GemdError, GemdValueError, GemdBoundsError, GemdValidationError,
    GemdEnumerationError, GemdSerializationError, GemdTypeError,
    GemdUnitError, GemdIncompatibleUnitsError, GemdUndefinedUnitError,
    GemdKeyError,
)


def test_hierarchy_isinstance():
    """Every leaf exception is an instance of GemdError."""
    for cls in [GemdValueError, GemdBoundsError, GemdValidationError,
                GemdEnumerationError, GemdSerializationError,
                GemdTypeError, GemdUnitError,
                GemdIncompatibleUnitsError, GemdUndefinedUnitError,
                GemdKeyError]:
        exc = cls("test")
        assert isinstance(exc, GemdError)


def test_backward_compat_value_error():
    """Verify GemdValueError is caught by except ValueError."""
    with pytest.raises(ValueError):
        raise GemdValueError("bad value")


def test_backward_compat_type_error():
    """Verify GemdTypeError is caught by except TypeError."""
    with pytest.raises(TypeError):
        raise GemdTypeError("bad type")


def test_backward_compat_key_error():
    """Verify GemdKeyError is caught by except KeyError."""
    with pytest.raises(KeyError):
        raise GemdKeyError("bad key")


def test_bounds_error_is_value_error():
    """Verify GemdBoundsError is caught by except ValueError."""
    with pytest.raises(ValueError):
        raise GemdBoundsError("out of range")


def test_structured_attributes_value_error():
    """Verify GemdValueError stores structured data."""
    exc = GemdValueError(
        "bad", expected="int", received="str",
        context="field x", guidance="pass an int"
    )
    assert exc.expected == "int"
    assert exc.received == "str"
    assert exc.context == "field x"
    assert exc.guidance == "pass an int"
    assert str(exc) == "bad"


def test_structured_attributes_type_error():
    """Verify GemdTypeError stores structured data."""
    exc = GemdTypeError(
        "wrong type", expected_type=int, received_type=str
    )
    assert exc.expected_type is int
    assert exc.received_type is str


def test_structured_attributes_bounds_error():
    """Verify GemdBoundsError stores bounds and value."""
    exc = GemdBoundsError(
        "out of range", bounds="[0, 100]", value="200"
    )
    assert exc.bounds == "[0, 100]"
    assert exc.value == "200"


def test_top_level_imports():
    """Verify exception classes are importable from the top-level package."""
    from gemd import (  # noqa: F401
        GemdError, GemdValueError, GemdTypeError,
        GemdBoundsError, GemdValidationError,
        GemdEnumerationError, GemdSerializationError,
    )
