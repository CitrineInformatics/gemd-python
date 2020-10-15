"""Tests of the UniformInteger class."""
import pytest

from gemd.entity.value.nominal_integer import NominalInteger
from gemd.entity.bounds import IntegerBounds


def test_bounds_are_integers():
    """Value must be an integer."""
    NominalInteger(5)
    with pytest.raises(TypeError):
        NominalInteger(5.7)
    with pytest.raises(TypeError):
        NominalInteger("five")


def test_contains():
    """Test that bounds know if a Value is contained within it."""
    bounds = IntegerBounds(1, 3)
    assert bounds.contains(NominalInteger(2).to_bounds())
    assert not bounds.contains(NominalInteger(5).to_bounds())
