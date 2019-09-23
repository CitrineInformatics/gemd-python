"""Test RealBounds."""
import pytest

from taurus.entity.bounds.integer_bounds import IntegerBounds
from taurus.entity.bounds.real_bounds import RealBounds
from taurus.entity.value.nominal_categorical import NominalCategorical
from taurus.entity.value.nominal_real import NominalReal


def test_unit_validation():
    """Make sure validation works when there is no unit conversion."""
    dim = RealBounds(lower_bound=0, upper_bound=100, default_units="meter")
    assert dim.validate(NominalReal(50, "m"))
    assert not dim.validate(NominalReal(150, "m"))


def test_unit_conversion():
    """Make sure validation works when a unit conversion is involved."""
    dim = RealBounds(lower_bound=0, upper_bound=100, default_units="meter")
    assert dim.validate(NominalReal(5000, "cm"))
    assert not dim.validate(NominalReal(50, "km"))
    assert not dim.validate(NominalReal(50, "s"))


def test_boundsless():
    """Make sure validation works for boundless bounds."""
    dim = RealBounds(lower_bound=0, upper_bound=100, default_units="")
    assert dim.validate(NominalReal(50, ""))
    assert not dim.validate(NominalReal(-50, ""))


def test_non_prefix():
    """Make sure validation works when the units differ by more than a prefix."""
    dim2 = RealBounds(lower_bound=0, upper_bound=100, default_units="N")
    assert dim2.validate(NominalReal(50, "kg m / sec^2"))


def test_contains():
    """Make sure unit conversions are applied to boundss for contains."""
    dim = RealBounds(lower_bound=0, upper_bound=100, default_units="degC")
    dim2 = RealBounds(lower_bound=33, upper_bound=200, default_units="degF")
    assert dim.contains(dim2)


def test_contains_no_units():
    """Make sure contains handles boundsless values."""
    dim = RealBounds(lower_bound=0, upper_bound=100, default_units="")
    dim2 = RealBounds(lower_bound=0, upper_bound=100, default_units="")
    assert dim.contains(dim2)


def test_contains_incompatible_units():
    """Make sure contains returns false when the units don't match."""
    dim = RealBounds(lower_bound=0, upper_bound=100, default_units="m")
    dim2 = RealBounds(lower_bound=0, upper_bound=100, default_units="kJ")
    dim3 = RealBounds(lower_bound=0, upper_bound=100, default_units='')
    assert not dim.contains(dim2)
    assert not dim.contains(dim3)


def test_constructor_error():
    """Test that invalid real bounds cannot be constructed."""
    with pytest.raises(ValueError):
        RealBounds()

    with pytest.raises(ValueError):
        RealBounds(0, float("inf"), "meter")

    with pytest.raises(ValueError):
        RealBounds(0, 100)


def test_type_mismatch():
    """Test that incompatible types cannot be matched against RealBounds."""
    bounds = RealBounds(0, 1, default_units="meters")
    assert not bounds.validate(NominalCategorical("foo"))
    assert not bounds.contains(IntegerBounds(0, 1))
    with pytest.raises(TypeError):
        bounds.validate(0)
    with pytest.raises(TypeError):
        bounds.contains([.33, .66])
