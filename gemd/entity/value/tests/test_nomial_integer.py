"""Tests of the UniformInteger class."""
import pytest

from gemd.entity.value.nominal_integer import NominalInteger
from gemd.entity.bounds import IntegerBounds


def test_bounds_are_integers():
    """Value must be an integer."""
    NominalInteger(5)
    with pytest.raises(TypeError):
        NominalInteger(5.7)
    with pytest.raises(TypeError):
        NominalInteger("five")


def test_contains():
    """Test that bounds know if a Value is contained within it."""
    bounds = IntegerBounds(1, 3)
    assert bounds.contains(NominalInteger(2)._to_bounds())
    assert not bounds.contains(NominalInteger(5)._to_bounds())


def test_contains_with_units():
    """Test that bounds know if a Value is contained within it, including a unit check."""
    # same units
    units = "kilometer"
    bounds_with_units = IntegerBounds(1, 3, default_units=units)
    assert bounds_with_units.contains(NominalInteger(2, units=units)._to_bounds())

    # Different units, with conversion
    assert not bounds_with_units.contains(NominalInteger(999, units="meter")._to_bounds())
    assert bounds_with_units.contains(NominalInteger(1000, units="meter")._to_bounds())
    assert bounds_with_units.contains(NominalInteger(3000, units="meter")._to_bounds())
    assert not bounds_with_units.contains(NominalInteger(3001, units="meter")._to_bounds())

    # A dimensionless bounds compared to a dimensional one
    with pytest.raises(ValueError):
        bounds_dimensionless = IntegerBounds(1, 3)
        bounds_dimensionless.contains(NominalInteger(2, units="parsec")._to_bounds())

    # A dimensional bounds compared to a dimensionless one
    with pytest.raises(ValueError):
        bounds_dimensionless = IntegerBounds(1, 3, default_units=units)
        bounds_dimensionless.contains(NominalInteger(2)._to_bounds())
