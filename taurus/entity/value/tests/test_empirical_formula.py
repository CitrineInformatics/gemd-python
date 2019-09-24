"""Test parsing and serde of empirical chemical formulae."""
from taurus.client.json_encoder import dumps, loads
from taurus.entity.value.empirical_formula import EmpiricalFormula


def test_all_elements():
    """Check that we can parse a simple formula with only integer stoichiometries."""
    for el in ["H", "He", "C", "Si"]:
        assert el in EmpiricalFormula.all_elements(), "Couldn't find {} in all_elements".format(el)
    assert len(EmpiricalFormula.all_elements()) == 103, "Expected 103 elements"


def test_json():
    """Check that we can json ser/de round-robin."""
    empirical = EmpiricalFormula("Al94.5Si5.5")
    copy = loads(dumps(empirical))
    assert(copy == empirical)
