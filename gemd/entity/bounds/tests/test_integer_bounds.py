"""Test IntegerBounds."""
import pytest

from gemd.entity.bounds.integer_bounds import IntegerBounds
from gemd.entity.bounds.real_bounds import RealBounds


def test_errors():
    """Make sure invalid bounds raise value errors."""
    with pytest.raises(ValueError):
        IntegerBounds()

    with pytest.raises(ValueError):
        IntegerBounds(0, float("inf"))

    with pytest.raises(ValueError):
        IntegerBounds(10, 1)


def test_incompatible_types():
    """Make sure that incompatible types aren't contained or validated."""
    int_bounds = IntegerBounds(0, 1)

    assert not int_bounds.contains(RealBounds(0.0, 1.0, ''))


def test_contains():
    """Test contains logic."""
    int_bounds = IntegerBounds(0, 2)

    assert int_bounds.contains(IntegerBounds(0, 1))
    assert int_bounds.contains(IntegerBounds(1, 2))
    assert not int_bounds.contains(IntegerBounds(1, 3))
    assert not int_bounds.contains(None)
    with pytest.raises(TypeError):
        int_bounds.contains([0, 1])

    from gemd.entity.value import NominalInteger

    assert int_bounds.contains(NominalInteger(1))
    assert not int_bounds.contains(NominalInteger(5))


def test_default_units():
    """Test optional default units"""
    units = "meter"
    no_units = IntegerBounds(0, 2)
    has_units = IntegerBounds(0, 2, default_units=units)

    assert no_units.default_units == "dimensionless"
    assert has_units.default_units == units

    new_units = "kilometer"
    has_units.default_units = new_units
    assert has_units.default_units == new_units
