"""Test IntegerBounds."""
import pytest

from gemd.entity.bounds.integer_bounds import IntegerBounds
from gemd.entity.bounds.base_bounds import DIMENSIONLESS
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


def test_contains_with_modified_units():
    """Test optional default units being converted."""
    units = "kilometer"
    has_units = IntegerBounds(0, 2, default_units=units)

    assert IntegerBounds(0, 2).default_units == DIMENSIONLESS
    assert IntegerBounds(0, 2, default_units="").default_units == DIMENSIONLESS
    assert has_units.default_units == units

    with pytest.raises(ValueError):
        bounds = IntegerBounds(0, 2)
        bounds.default_units = None

    new_units = "meter"
    has_units.default_units = new_units
    assert has_units.default_units == new_units


def test_contains_units_comparison():
    """Test optional default units being compared."""
    units = "kilometer"
    bounds = IntegerBounds(0, 2, default_units=units)

    assert bounds.contains(bounds)
    assert bounds.contains(IntegerBounds(0, 2000, default_units="meter"))
    assert not bounds.contains(IntegerBounds(0, 2001, default_units="meter"))
    assert not bounds.contains(IntegerBounds(-1, 2000, default_units="meter"))
    assert not bounds.contains(RealBounds(0, 2000, default_units="meter"))
    assert not bounds.contains(None)

    with pytest.raises(ValueError):
        # Cannot compare dimensionless with "kilometers"
        bounds.contains(IntegerBounds(0, 2000))
