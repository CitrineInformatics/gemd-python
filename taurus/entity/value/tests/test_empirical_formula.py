"""Test parsing and serde of empirical chemical formulae."""
import pytest

from taurus.client.json_encoder import dumps, loads
from taurus.entity.value.empirical_formula import EmpiricalFormula


def test_all_elements():
    """Check that list of all elements exists and has some select examples."""
    for el in ["H", "He", "C", "Si", "Mg", "Al", "Co", "Ce"]:
        assert el in EmpiricalFormula.all_elements(), "Couldn't find {} in all_elements".format(el)
    assert len(EmpiricalFormula.all_elements()) == 103, "Expected 103 elements"


def test_json():
    """Check that we can json ser/de round-robin."""
    empirical = EmpiricalFormula("Al94.5Si5.5")
    copy = loads(dumps(empirical))
    assert(copy == empirical)


def test_formula_setter():
    """Check that we can set the formula."""
    test_formula = "CsPbBr1.5I1.5"
    test_empirical = EmpiricalFormula()
    assert test_empirical.formula is None
    test_empirical.formula = test_formula
    assert test_empirical.formula == test_formula


def test_invalid_formula():
    """Check that an invalid formula throws a TypeError."""
    with pytest.raises(TypeError):
        EmpiricalFormula(formula={"Al": 2, "O": 3})
