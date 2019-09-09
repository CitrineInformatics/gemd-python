"""Test IntegerBounds."""
import pytest

from taurus.entity.bounds.integer_bounds import IntegerBounds
from taurus.entity.bounds.real_bounds import RealBounds
from taurus.entity.value.nominal_integer import NominalInteger
from taurus.entity.value.nominal_real import NominalReal
from taurus.entity.value.uniform_integer import UniformInteger


def test_errors():
    """Make sure invalid bounds raise value errors."""
    with pytest.raises(ValueError):
        IntegerBounds()

    with pytest.raises(ValueError):
        IntegerBounds(0, float("inf"))


def test_incompatible_types():
    """Make sure that incompatible types aren't contained or validated."""
    int_bounds = IntegerBounds(0, 1)

    assert not int_bounds.validate(NominalReal(0.0, ''))

    assert not int_bounds.contains(RealBounds(0.0, 1.0, ''))


def test_validate():
    """Test validation logic."""
    int_bounds = IntegerBounds(0, 2)

    assert int_bounds.validate(NominalInteger(0))
    assert int_bounds.validate(NominalInteger(2))
    assert not int_bounds.validate(NominalInteger(3))

    assert not int_bounds.validate(UniformInteger(0, 3))
    with pytest.raises(TypeError):
        int_bounds.validate(0)


def test_contains():
    """Test contains logic."""
    int_bounds = IntegerBounds(0, 2)

    assert int_bounds.contains(IntegerBounds(0, 1))
    assert int_bounds.contains(IntegerBounds(1, 2))
    assert not int_bounds.contains(IntegerBounds(1, 3))
    with pytest.raises(TypeError):
        int_bounds.contains([0, 1])
