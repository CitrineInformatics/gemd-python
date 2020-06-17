"""Tests of the ingredient run object."""
import pytest

from gemd.entity.object.ingredient_run import IngredientRun
from gemd.entity.object.process_run import ProcessRun
from gemd.entity.bounds.real_bounds import RealBounds


def test_ingredient_reassignment():
    """Check that an ingredient run can be re-assigned to a new process run."""
    boiling = ProcessRun("Boil potatoes")
    frying = ProcessRun("Fry potatoes")
    oil = IngredientRun(process=boiling)
    potatoes = IngredientRun(process=boiling)
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


def test_invalid_assignment():
    """Invalid assignments to `process` or `material` throw a TypeError."""
    with pytest.raises(TypeError):
        IngredientRun(material=RealBounds(0, 5.0, ''))
    with pytest.raises(TypeError):
        IngredientRun(process="process")
    with pytest.raises(TypeError):
        IngredientRun(spec=5)
    with pytest.raises(TypeError):
        IngredientRun(name="Flour")  # IngredientRuns don't have their own name
