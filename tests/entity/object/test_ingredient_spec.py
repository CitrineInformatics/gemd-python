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
from gemd.entity.bounds_validation import validation_level, WarningLevel


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


VALID_FRACTIONS = [
    NominalReal(1.0, ''),
    UniformReal(0.5, 0.6, ''),
    NormalReal(0.2, 0.3, '')
]

INVALID_FRACTIONS = [
    NominalReal(1.0, 'm'),
    UniformReal(0.7, 1.1, ''),
    NormalReal(-0.2, 0.3, '')
]

VALID_QUANTITIES = [
    NominalReal(14.0, 'g'),
    UniformReal(0.5, 0.6, 'mol'),
    NormalReal(0.3, 0.6, 'cc')
]

INVALID_QUANTITIES = [
    NominalReal(14.0, ''),
    UniformReal(-0.1, 0.3, 'mol'),
]

INVALID_TYPES = [
    NominalCategorical("blue"),
    NominalInteger(5),
    EmpiricalFormula("CH4"),
    0.33,
    "0.5"
]


@pytest.mark.parametrize("valid_fraction", VALID_FRACTIONS)
def test_valid_fractions(valid_fraction, caplog):
    """
    Check that all fractional quantities must be continuous values.
    """
    with validation_level(WarningLevel.WARNING):
        ingred = IngredientSpec(name="name", mass_fraction=valid_fraction)
        assert ingred.mass_fraction == valid_fraction
        ingred = IngredientSpec(name="name", volume_fraction=valid_fraction)
        assert ingred.volume_fraction == valid_fraction
        ingred = IngredientSpec(name="name", number_fraction=valid_fraction)
        assert ingred.number_fraction == valid_fraction
        assert ingred.absolute_quantity is None
    assert len(caplog.records) == 0, "Warned on valid values with WARNING."


@pytest.mark.parametrize("valid_quantity", VALID_QUANTITIES)
def test_valid_quantities(valid_quantity, caplog):
    """
    Check that all quantities must be continuous values.
    """
    with validation_level(WarningLevel.WARNING):
        ingred = IngredientSpec(name="name", absolute_quantity=valid_quantity)
        assert ingred.absolute_quantity == valid_quantity
        assert ingred.mass_fraction is None
        assert ingred.number_fraction is None
        assert ingred.volume_fraction is None
    assert len(caplog.records) == 0, "Warned on valid values with WARNING."


@pytest.mark.parametrize("invalid_fraction", INVALID_FRACTIONS)
def test_invalid_fractions(invalid_fraction, caplog):
    """
    Verify that when validation is requested, limits are enforced for fractions.
    """
    with validation_level(WarningLevel.IGNORE):
        IngredientSpec(name="name", mass_fraction=invalid_fraction)
    assert len(caplog.records) == 0, f"Warned on invalid values with IGNORE: {invalid_fraction}"
    with validation_level(WarningLevel.WARNING):
        IngredientSpec(name="name", mass_fraction=invalid_fraction)
    assert len(caplog.records) == 1, f"Didn't warn on invalid values with IGNORE: {invalid_fraction}"
    with validation_level(WarningLevel.FATAL):
        with pytest.raises(ValueError):
            IngredientSpec(name="name", mass_fraction=invalid_fraction)


@pytest.mark.parametrize("invalid_quantity", INVALID_QUANTITIES)
def test_invalid_quantities(invalid_quantity, caplog):
    """
    Verify that when validation is requested, limits are enforced for fractions.
    """
    with validation_level(WarningLevel.IGNORE):
        IngredientSpec(name="name", absolute_quantity=invalid_quantity)
    assert len(caplog.records) == 0, f"Warned on invalid values with IGNORE: {invalid_quantity}"
    with validation_level(WarningLevel.WARNING):
        IngredientSpec(name="name", absolute_quantity=invalid_quantity)
    assert len(caplog.records) == 1, f"Didn't warn on invalid values with IGNORE: {invalid_quantity}"
    with validation_level(WarningLevel.FATAL):
        with pytest.raises(ValueError):
            IngredientSpec(name="name", absolute_quantity=invalid_quantity)


@pytest.mark.parametrize("invalid_type", INVALID_TYPES)
def test_invalid_types(invalid_type):
    """Check that any non-continuous value for a quantity throws a TypeError."""
    with pytest.raises(TypeError):
        IngredientSpec(name="name", mass_fraction=invalid_type)
    with pytest.raises(TypeError):
        IngredientSpec(name="name", volume_fraction=invalid_type)
    with pytest.raises(TypeError):
        IngredientSpec(name="name", number_fraction=invalid_type)
    with pytest.raises(TypeError):
        IngredientSpec(name="name", absolute_quantity=invalid_type)


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
