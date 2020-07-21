"""Tests of the UniformInteger class."""
import pytest

from gemd.entity.value.nominal_integer import NominalInteger


def test_bounds_are_integers():
    """Value must be an integer."""
    with pytest.raises(AssertionError):
        NominalInteger(5.7)
    with pytest.raises(ValueError):
        NominalInteger("five")
