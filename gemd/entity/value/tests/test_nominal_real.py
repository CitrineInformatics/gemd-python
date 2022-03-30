"""Tests of the NominalReal class."""
from gemd.entity.value.nominal_real import NominalReal
from gemd.entity.bounds import RealBounds


def test_contains():
    """Test that bounds know if a Value is contained within it."""
    bounds = RealBounds(1, 3, 'm')
    assert not bounds.contains(NominalReal(99, 'cm')._to_bounds())
    assert bounds.contains(NominalReal(100, 'cm')._to_bounds())
    assert bounds.contains(NominalReal(200, 'cm')._to_bounds())
    assert bounds.contains(NominalReal(300, 'cm')._to_bounds())
    assert not bounds.contains(NominalReal(301, 'cm')._to_bounds())
    assert not bounds.contains(NominalReal(4, 'm')._to_bounds())
