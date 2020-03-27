"""Tests of the NominalCategorical class."""
from gemd.entity.value.nominal_categorical import NominalCategorical


def test_category_setter():
    """Test that the category can be set."""
    test_category = "salt"
    test_categorical = NominalCategorical()
    assert test_categorical.category is None
    test_categorical.category = test_category
    assert test_categorical.category == test_category
