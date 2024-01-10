"""Test IntegerBounds."""
import pytest

from gemd.entity.bounds.integer_bounds import IntegerBounds
from gemd.entity.bounds.real_bounds import RealBounds
from gemd.entity.value.nominal_integer import NominalInteger


def test_errors():
    """Make sure invalid bounds raise value errors."""
    with pytest.raises(TypeError):
        IntegerBounds()

    with pytest.raises(ValueError):
        IntegerBounds(float("-inf"), 0)

    with pytest.raises(ValueError):
        IntegerBounds(0, float("inf"))

    with pytest.raises(ValueError):
        IntegerBounds(10, 1)

    with pytest.raises(ValueError):
        bnd = IntegerBounds(0, 1)
        bnd.lower_bound = 10


def test_incompatible_types():
    """Make sure that incompatible types aren't contained or validated."""
    int_bounds = IntegerBounds(0, 1)

    assert not int_bounds.contains(RealBounds(0.0, 1.0, ''))


def test_contains():
    """Test contains logic."""
    int_bounds = IntegerBounds(0, 2)

    assert int_bounds.contains(IntegerBounds(0, 1))
    assert int_bounds.contains(IntegerBounds(1, 2))
    assert not int_bounds.contains(IntegerBounds(1, 3))
    assert not int_bounds.contains(None)
    with pytest.raises(TypeError):
        int_bounds.contains([0, 1])

    assert int_bounds.contains(NominalInteger(1))
    assert not int_bounds.contains(NominalInteger(5))


def test_union():
    """Test basic union & update logic."""
    bounds = IntegerBounds(lower_bound=1, upper_bound=5)
    low = NominalInteger(0)
    high = NominalInteger(10)
    assert bounds.union(low).contains(low), "Bounds didn't get low value"
    assert bounds.union(high).contains(high), "Bounds didn't get high value"
    assert bounds.union(low, high).contains(bounds), "Bounds didn't keep old values"
    assert not bounds.contains(low), "Bounds got updated"

    bounds.update(low)
    assert bounds.contains(low), "Bounds didn't get updated"

    with pytest.raises(TypeError):
        bounds.union(RealBounds(0, 1, ""))
