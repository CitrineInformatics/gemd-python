"""Tests of the ingredient spec object."""
from taurus.entity.object.ingredient_spec import IngredientSpec
from taurus.entity.object.process_spec import ProcessSpec


def test_ingredient_reassignment():
    """Check that an ingredient spec can be re-assigned to a new process spec."""
    boiling = ProcessSpec("Boil potatoes")
    frying = ProcessSpec("Fry potatoes")
    oil = IngredientSpec(name="Oil", process=boiling)
    potatoes = IngredientSpec(name="Potatoes", process=boiling)
    assert oil.process == boiling
    assert set(boiling.ingredients) == {oil, potatoes}
    assert frying.ingredients == []

    oil.process = frying
    assert oil.process == frying
    assert boiling.ingredients == [potatoes]
    assert frying.ingredients == [oil]

    potatoes.process = frying
    assert potatoes.process == frying
    assert boiling.ingredients == []
    assert set(frying.ingredients) == {oil, potatoes}
