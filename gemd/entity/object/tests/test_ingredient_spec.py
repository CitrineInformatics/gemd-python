"""Tests of the ingredient spec object."""
import pytest

from gemd.entity.object.ingredient_spec import IngredientSpec
from gemd.entity.object.process_spec import ProcessSpec
from gemd.entity.value.nominal_real import NominalReal
from gemd.entity.value.uniform_real import UniformReal
from gemd.entity.value.normal_real import NormalReal
from gemd.entity.value.nominal_integer import NominalInteger
from gemd.entity.value.nominal_categorical import NominalCategorical
from gemd.entity.value.empirical_formula import EmpiricalFormula


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


VALID_QUANTITIES = [
    NominalReal(14.0, ''),
    UniformReal(0.5, 0.6, 'm'),
    NormalReal(-0.3, 0.6, "kg")
]

INVALID_QUANTITIES = [
    NominalCategorical("blue"),
    NominalInteger(5),
    EmpiricalFormula("CH4"),
    0.33,
    "0.5"
]


@pytest.mark.parametrize("valid_quantity", VALID_QUANTITIES)
def test_valid_quantities(valid_quantity):
    """
    Check that all quantities must be continuous values.

    There are no restrictions on the value or the units. Although a volume fraction of -5 kg
    does not make physical sense, it will not throw an error.
    """
    ingred = IngredientSpec(name="name", mass_fraction=valid_quantity)
    assert ingred.mass_fraction == valid_quantity
    ingred = IngredientSpec(name="name", volume_fraction=valid_quantity)
    assert ingred.volume_fraction == valid_quantity
    ingred = IngredientSpec(name="name", number_fraction=valid_quantity)
    assert ingred.number_fraction == valid_quantity
    ingred = IngredientSpec(name="name", absolute_quantity=valid_quantity)
    assert ingred.absolute_quantity == valid_quantity


@pytest.mark.parametrize("invalid_quantity", INVALID_QUANTITIES)
def test_invalid_quantities(invalid_quantity):
    """Check that any non-continuous value for a quantity throws a TypeError."""
    with pytest.raises(TypeError):
        IngredientSpec(name="name", mass_fraction=invalid_quantity)
    with pytest.raises(TypeError):
        IngredientSpec(name="name", volume_fraction=invalid_quantity)
    with pytest.raises(TypeError):
        IngredientSpec(name="name", number_fraction=invalid_quantity)
    with pytest.raises(TypeError):
        IngredientSpec(name="name", absolute_quantity=invalid_quantity)


def test_invalid_assignment():
    """Invalid assignments to `process` or `material` throw a TypeError."""
    with pytest.raises(TypeError):
        IngredientSpec(name="name", material=NominalReal(3, ''))
    with pytest.raises(TypeError):
        IngredientSpec(name="name", process="process")
    with pytest.raises(TypeError):
        IngredientSpec()  # Name is required


def test_bad_has_template():
    """Make sure the non-implementation of HasTemplate behaves properly."""
    assert isinstance(None, IngredientSpec(name="name")._template_type()), \
        "Ingredients didn't have NoneType templates"
    assert IngredientSpec(name="name").template is None, \
        "An ingredient didn't have a null template."
    with pytest.raises(AttributeError):  # Note an AttributeError, not a TypeError
        IngredientSpec(name="name").template = 1
