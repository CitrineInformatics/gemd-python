"""Tests of the NormalReal class."""
from gemd.entity.value.normal_real import NormalReal
from gemd.entity.bounds import RealBounds


def test_contains():
    """Test that bounds know if a Value is contained within it."""
    bounds = RealBounds(1, 3, "m")
    assert bounds.contains(NormalReal(300, 10, "cm")._to_bounds())
    assert not bounds.contains(NormalReal(5, 0.1, "m")._to_bounds())
