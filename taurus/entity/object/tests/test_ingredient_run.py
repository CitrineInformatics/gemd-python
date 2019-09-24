"""Tests of the ingredient run object."""
from taurus.entity.object.ingredient_run import IngredientRun
from taurus.entity.object.process_run import ProcessRun


def test_ingredient_reassignment():
    """Check that an ingredient run can be re-assigned to a new process run."""
    boiling = ProcessRun("Boil potatoes")
    frying = ProcessRun("Fry potatoes")
    oil = IngredientRun(name="Oil", process=boiling)
    potatoes = IngredientRun(name="Potatoes", process=boiling)
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
