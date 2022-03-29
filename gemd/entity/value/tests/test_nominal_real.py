"""Tests of the NominalReal class."""
import pytest

from gemd.entity.value.nominal_real import NominalReal
from gemd.entity.bounds import RealBounds


def test_contains():
    """Test that bounds know if a Value is contained within it."""
    bounds = RealBounds(1, 3, 'm')
    assert bounds.contains(NominalReal(200, 'cm')._to_bounds())
    assert not bounds.contains(NominalReal(5, 'm')._to_bounds())

    # A dimensionless bounds compared to a dimensional one
    with pytest.raises(ValueError):
        bounds_dimensionless = RealBounds(1, 3)
        bounds_dimensionless.contains(RealBounds(2, units='parsec')._to_bounds())

    # A dimensional bounds compared to a dimensionless one
    with pytest.raises(ValueError):
        bounds_dimensional = RealBounds(1, 3, default_units='m')
        bounds_dimensional.contains(RealBounds(2)._to_bounds())
