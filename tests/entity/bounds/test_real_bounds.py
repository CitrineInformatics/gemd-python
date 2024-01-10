"""Test RealBounds."""
import pytest

from gemd.entity.bounds.integer_bounds import IntegerBounds
from gemd.entity.bounds.real_bounds import RealBounds
from gemd.entity.value.nominal_real import NominalReal
from gemd.units import IncompatibleUnitsError


def test_contains():
    """Make sure unit conversions are applied to bounds for contains."""
    dim = RealBounds(lower_bound=0, upper_bound=100, default_units="degC")
    dim2 = RealBounds(lower_bound=33, upper_bound=200, default_units="degF")
    assert dim.contains(dim2)

    assert dim.contains(NominalReal(5, 'degC'))
    assert not dim.contains(NominalReal(5, 'K'))


def test_union():
    """Test basic union & update logic."""
    bounds = RealBounds(lower_bound=1, upper_bound=5, default_units='mm')
    low = RealBounds(lower_bound=1, upper_bound=5, default_units='um')
    high = NominalReal(1, 'cm')
    bad = NominalReal(1, 'kg')
    assert bounds.union(low).contains(low), "Bounds didn't get low value"
    assert bounds.union(high).contains(high), "Bounds didn't get high value"
    assert bounds.union(low, high).contains(bounds), "Bounds didn't keep old values"
    assert not bounds.contains(low), "Bounds got updated"

    bounds.update(low)
    assert bounds.contains(low), "Bounds didn't get updated"

    with pytest.raises(IncompatibleUnitsError):
        bounds.update(bad)
    assert not bounds.contains(bad), "Bounds had bad in bounds."

    with pytest.raises(TypeError):
        bounds.union(IntegerBounds(0, 1))


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
    with pytest.raises(TypeError):
        RealBounds()

    with pytest.raises(ValueError):
        RealBounds(lower_bound=0, upper_bound=float("inf"), default_units="meter")

    with pytest.raises(ValueError):
        RealBounds(lower_bound=None, upper_bound=10, default_units='')

    with pytest.raises(ValueError):
        RealBounds(lower_bound=0, upper_bound=100, default_units=None)

    with pytest.raises(ValueError):
        RealBounds(lower_bound=100, upper_bound=0, default_units="m")

    with pytest.raises(ValueError):
        bnd = RealBounds(lower_bound=0, upper_bound=10, default_units="m")
        bnd.lower_bound = 100


def test_type_mismatch():
    """Test that incompatible types cannot be matched against RealBounds."""
    bounds = RealBounds(0, 1, default_units="meters")
    assert not bounds.contains(IntegerBounds(0, 1))
    assert not bounds.contains(None)
    with pytest.raises(TypeError):
        bounds.contains([.33, .66])
