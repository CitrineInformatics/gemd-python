"""Tests of the UniformInteger class."""
import pytest

from gemd.entity.value.nominal_integer import NominalInteger


def test_bounds_are_integers():
    """Value must be an integer."""
    NominalInteger(5)
    with pytest.raises(TypeError):
        NominalInteger(5.7)
    with pytest.raises(TypeError):
        NominalInteger("five")
