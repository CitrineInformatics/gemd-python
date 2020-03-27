"""Tests of the DiscreteCategorical class."""
import pytest

from gemd.entity.value.discrete_categorical import DiscreteCategorical


def test_probabilities_setter():
    """Test that the probabilities can be set."""
    test_probabilities = {"solid": 0.9, "liquid": 0.1}
    test_categorical = DiscreteCategorical()
    assert test_categorical.probabilities is None
    test_categorical.probabilities = test_probabilities
    assert test_categorical.probabilities == test_probabilities


def test_invalid_assignment():
    """Test that invalid assignment throws the appropriate error."""
    with pytest.raises(TypeError):
        DiscreteCategorical(probabilities=["solid", "liquid"])
    with pytest.raises(ValueError):
        DiscreteCategorical(probabilities={"solid": 0.9, "liquid": 0.2})
