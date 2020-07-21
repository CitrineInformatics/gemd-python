"""Tests of the UniformInteger class."""
import pytest

from gemd.entity.value.uniform_integer import UniformInteger


def test_bounds_order():
    """Lower bound must be <= upper bound."""
    UniformInteger(3, 7)
    UniformInteger(12, 12)
    with pytest.raises(AssertionError):
        UniformInteger(22, 18)


def test_bounds_are_integers():
    """Lower bound and upper bound must be integers."""
    with pytest.raises(AssertionError):
        UniformInteger(5.7, 10)
    with pytest.raises(ValueError):
        UniformInteger(1, "five")
