"""Test parsing and serde of empirical chemical formulae."""
from taurus.client.json_encoder import dumps, loads
from taurus.entity.value.empirical_formula import EmpiricalFormula


def test_parse():
    """Check that we can parse a simple formula with only integer stoichiometries."""
    empirical = EmpiricalFormula("CH4")
    assert(empirical.components == {"C", "H"})
    assert(empirical.quantities["H"] == 4 * empirical.quantities["C"])


def test_fractional():
    """Check that we can parse a formula with fractional stoichiometries."""
    empirical = EmpiricalFormula("Al94.5Si5.5")
    assert(empirical.components == {"Al", "Si"})
    assert(empirical.quantities["Al"] == 94.5)
    assert(empirical.quantities["Si"] == 5.5)


def test_json():
    """Check that we can json ser/de round-robin."""
    empirical = EmpiricalFormula("Al94.5Si5.5")
    copy = loads(dumps(empirical))
    assert(copy == empirical)
