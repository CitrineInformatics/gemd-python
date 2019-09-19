"""Test RealBounds."""
import pytest

from taurus.entity.bounds.integer_bounds import IntegerBounds
from taurus.entity.bounds.real_bounds import RealBounds


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
    assert not bounds.contains(IntegerBounds(0, 1))
