"""Tests of the NominalCategorical class."""
from gemd.entity.value.nominal_categorical import NominalCategorical
from gemd.entity.bounds import CategoricalBounds


def test_category_setter():
    """Test that the category can be set."""
    test_category = "salt"
    test_categorical = NominalCategorical()
    assert test_categorical.category is None
    test_categorical.category = test_category
    assert test_categorical.category == test_category


def test_contains():
    """Test that bounds know if a Value is contained within it."""
    bounds = CategoricalBounds({"solid", "liquid"})
    assert bounds.contains(NominalCategorical("solid").to_bounds())
    assert not bounds.contains(NominalCategorical("gas").to_bounds())
