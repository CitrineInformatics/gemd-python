"""Tests of the NominalComposition class."""
import pytest

from gemd.entity.value.nominal_composition import NominalComposition
from gemd.entity.bounds import CompositionBounds


def test_quantities_are_dict():
    """Test that NominalComposition can be instantiated several ways, all producing a dict."""
    test_composition = NominalComposition()
    assert isinstance(test_composition.quantities, dict)
    test_composition = NominalComposition(dict(acetone=0.25, methanol=0.75))
    assert isinstance(test_composition.quantities, dict)
    test_composition = NominalComposition([["gas", 0.7], ["plasma", 0.3]])
    assert isinstance(test_composition.quantities, dict)


def test_invalid_assignment():
    """Test that invalid assignment produces a TypeError."""
    with pytest.raises(TypeError):
        NominalComposition(("a quantity", 55))


def test_contains():
    """Test that bounds know if a Value is contained within it."""
    bounds = CompositionBounds({"acetone", "methanol"})
    assert bounds.contains(NominalComposition(dict(acetone=0.25, methanol=0.75))._to_bounds())
    assert not bounds.contains(NominalComposition(dict(acetone=0.25, water=0.75))._to_bounds())
