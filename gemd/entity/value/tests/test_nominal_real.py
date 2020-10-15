"""Tests of the NominalReal class."""
from gemd.entity.value.nominal_real import NominalReal
from gemd.entity.bounds import RealBounds


def test_contains():
    """Test that bounds know if a Value is contained within it."""
    bounds = RealBounds(1, 3, 'm')
    assert bounds.contains(NominalReal(200, 'cm').to_bounds())
    assert not bounds.contains(NominalReal(5, 'm').to_bounds())
