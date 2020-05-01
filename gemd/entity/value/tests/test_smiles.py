"""Test parsing and serde of empirical chemical formulae."""
import pytest

from gemd.json import dumps, loads
from gemd.entity.value.smiles_value import SMILES


def test_json():
    """Check that we can json ser/de round-robin."""
    smiles = SMILES("c1(C=O)cc(OC)c(O)cc1")
    copy = loads(dumps(smiles))
    assert(copy == smiles)


def test_smiles_setter():
    """Check that we can set the formula."""
    test_struct = "c1(C=O)cc(OC)c(O)cc1"
    test_smiles = SMILES()
    assert test_smiles.smiles is None
    test_smiles.smiles = test_struct
    assert test_smiles.smiles == test_struct


def test_invalid_smiles():
    """
    Check that an invalid SMILES throws a TypeError.

    Note that real checking requires an external package.
    """
    with pytest.raises(TypeError):
        SMILES({"Al": 2, "O": 3})
