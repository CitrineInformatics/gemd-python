"""Tests of the UniformInteger class."""
import pytest

from gemd.entity.value.uniform_integer import UniformInteger
from gemd.entity.bounds import IntegerBounds


def test_bounds_order():
    """Lower bound must be <= upper bound."""
    UniformInteger(3, 7)
    UniformInteger(12, 12)
    with pytest.raises(ValueError):
        UniformInteger(22, 18)
    with pytest.raises(ValueError):
        UniformInteger(3, 7).lower_bound = 10
    with pytest.raises(ValueError):
        UniformInteger(3, 7).upper_bound = 1


def test_bounds_are_integers():
    """Lower bound and upper bound must be integers."""
    with pytest.raises(TypeError):
        UniformInteger(5.7, 10)
    with pytest.raises(TypeError):
        UniformInteger(1, "five")


def test_contains():
    """Test that bounds know if a Value is contained within it."""
    bounds = IntegerBounds(1, 3)
    assert bounds.contains(UniformInteger(1, 2)._to_bounds())
    assert not bounds.contains(UniformInteger(3, 5)._to_bounds())
