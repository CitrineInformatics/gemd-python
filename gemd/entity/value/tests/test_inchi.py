"""Test parsing and serde of an InChI molecular structure."""
import pytest

from gemd.json import dumps, loads
from gemd.entity.value.inchi_value import InChI
from gemd.entity.bounds import MolecularStructureBounds


def test_json():
    """Check that we can json ser/de round-robin."""
    inchi = InChI("InChI=1/C8H8O3/c1-11-8-4-6(5-9)2-3-7(8)10/h2-5,10H,1H3")
    copy = loads(dumps(inchi))
    assert(copy == inchi)


def test_inchi_setter():
    """Check that we can set the inchi."""
    test_struct = "InChI=1/C8H8O3/c1-11-8-4-6(5-9)2-3-7(8)10/h2-5,10H,1H3"
    test_inchi = InChI()
    assert test_inchi.inchi is None
    test_inchi.inchi = test_struct
    assert test_inchi.inchi == test_struct

    assert InChI("inchi=1/C8H8O3").inchi == "InChI=1/C8H8O3"
    assert InChI("C8H8O3").inchi == "InChI=1S/C8H8O3"
    # https://www.sigmaaldrich.com/US/en/product/aldrich/757136
    assert InChI("1S/C4BO8.Li").inchi == "InChI=1S/C4BO8.Li"


def test_invalid_inchi():
    """
    Check that an invalid InChI throws a TypeError.

    Note that real checking requires an external package.
    """
    with pytest.raises(TypeError):
        InChI({"Al": 2, "O": 3})


def test_contains():
    """Test that bounds know if a Value is contained within it."""
    bounds = MolecularStructureBounds()
    inchi = InChI("InChI=1/C8H8O3/c1-11-8-4-6(5-9)2-3-7(8)10/h2-5,10H,1H3")
    assert bounds.contains(inchi._to_bounds())
