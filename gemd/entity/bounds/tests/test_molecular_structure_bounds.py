"""Test of CategoricalBounds."""
import pytest

from gemd.json import dumps, loads
from gemd.entity.bounds.molecular_structure_bounds import MolecularStructureBounds
from gemd.entity.bounds.real_bounds import RealBounds


def test_contains():
    """Test basic contains logic."""
    bounds = MolecularStructureBounds()
    assert bounds.contains(MolecularStructureBounds())
    assert not bounds.contains(RealBounds(0.0, 2.0, ''))
    assert not bounds.contains(None)
    with pytest.raises(TypeError):
        bounds.contains('c1(C=O)cc(OC)c(O)cc1')
    with pytest.raises(TypeError):
        bounds.contains('InChI=1/C8H8O3/c1-11-8-4-6(5-9)2-3-7(8)10/h2-5,10H,1H3')

    from gemd.entity.value import Smiles, NominalInteger

    assert bounds.contains(Smiles('c1(C=O)cc(OC)c(O)cc1'))
    assert not bounds.contains(NominalInteger(5))


def test_json():
    """Test that serialization works (empty dictionary)."""
    bounds = MolecularStructureBounds()
    copy = loads(dumps(bounds))
    assert copy == bounds
