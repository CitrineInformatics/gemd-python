"""Tests of the material spec object."""
import pytest

from taurus.entity.object.process_spec import ProcessSpec
from taurus.entity.object.material_spec import MaterialSpec


def test_process_reassignment():
    """Test that a material can be assigned to a new process."""
    drying = ProcessSpec("drying")
    welding = ProcessSpec("welding")
    powder = MaterialSpec("Powder", process=welding)

    assert powder.process == welding
    assert welding.output_material == powder

    powder.process = drying
    assert powder.process == drying
    assert drying.output_material == powder
    assert welding.output_material is None


def test_invalid_assignment():
    """Invalid assignments to `process` or `template` throw a ValueError."""
    with pytest.raises(ValueError):
        MaterialSpec("name", process=["Process 1", "Process 2"])
    with pytest.raises(ValueError):
        MaterialSpec("name", template=MaterialSpec("another spec"))
