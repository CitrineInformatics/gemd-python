"""Tests of the UniformReal class."""
import pytest

from gemd.entity.value.uniform_real import UniformReal
from gemd.entity.bounds import RealBounds


def test_bounds_order():
    """Lower bound must be <= upper bound."""
    UniformReal(4.4, 8.8, 'm')
    UniformReal(100.0, 100.0, 'm')
    with pytest.raises(AssertionError):
        UniformReal(23.2, 18.9, 'm')


def test_equality():
    """Test that equality checks both bounds and units."""
    value1 = UniformReal(0, 1, '')
    value2 = UniformReal(0, 1, 'cm')
    value3 = UniformReal(0, 2, '')

    assert value1 == value1
    assert value1 != value2
    assert value1 != value3
    assert value1 != 0.5


def test_contains():
    """Test that bounds know if a Value is contained within it."""
    bounds = RealBounds(1, 3, 'm')
    assert bounds.contains(UniformReal(100, 200, 'cm').to_bounds())
    assert not bounds.contains(UniformReal(3, 5, 'm').to_bounds())
    assert not bounds.contains(UniformReal(1, 3, '').to_bounds())
