"""Tests of the material spec object."""
import pytest

from taurus.entity.object.process_spec import ProcessSpec
from taurus.entity.object.material_spec import MaterialSpec
from taurus.entity.attribute.property import Property
from taurus.entity.attribute.property_and_conditions import PropertyAndConditions
from taurus.entity.value.nominal_real import NominalReal


material_spec = MaterialSpec(
    name="test_material",
    properties=[
        PropertyAndConditions(
            property=Property(name="test_property", value=NominalReal(1.0, "kJ"))
        )
    ],
)


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
    """Invalid assignments to `process` or `template` throw a TypeError."""
    with pytest.raises(TypeError):
        MaterialSpec("name", process=["Process 1", "Process 2"])
    with pytest.raises(TypeError):
        MaterialSpec("name", template=MaterialSpec("another spec"))


def test_creating_material_run():
    """Test creating a material run from a material spec."""

    material = material_spec()  # inherit default attributes from spec
    assert material.name == material_spec.name
    assert material.spec is material_spec

    material = material_spec(name="other name")  # change default values
    assert material.name == "other name"
