"""Tests of the UniformReal class."""
import pytest

from taurus.entity.value.uniform_real import UniformReal


def test_bounds_order():
    """Lower bound must be <= upper bound."""
    UniformReal(4.4, 8.8, 'm')
    UniformReal(100.0, 100.0, 'm')
    with pytest.raises(AssertionError):
        UniformReal(23.2, 18.9, 'm')


def test_equality():
    """Test that equality checks both bounds and integers."""
    value1 = UniformReal(0, 1, '')
    value2 = UniformReal(0, 100, 'cm')
    value3 = UniformReal(0, 2, '')

    assert value1 == value1
    assert value1 != value2  # Equality check does not do unit conversion.
    assert value1 != value3
    assert value1 != 0.5
