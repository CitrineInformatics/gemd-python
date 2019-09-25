"""Tests of the NominalComposition class."""
import pytest

from taurus.entity.value.nominal_composition import NominalComposition


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


def test_quantities_as_dict():
    """Test that the as_dict() method represents `quantities` as a list."""
    test_composition = NominalComposition(dict(acetone=0.25, methanol=0.75))
    quantities = test_composition.as_dict().get('quantities')
    assert isinstance(quantities, list) and len(quantities) == 2
