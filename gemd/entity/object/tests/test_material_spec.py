"""Tests of the material spec object."""
import pytest

from gemd.entity.attribute import PropertyAndConditions, Property, Condition
from gemd.entity.bounds import IntegerBounds
from gemd.entity.object.process_spec import ProcessSpec
from gemd.entity.object.material_spec import MaterialSpec
from gemd.entity.template import MaterialTemplate, PropertyTemplate, ConditionTemplate
from gemd.entity.value import NominalInteger


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
    with pytest.raises(TypeError):
        MaterialSpec()  # Name is required


def test_dependences():
    """Test that dependency lists make sense."""
    prop = PropertyTemplate(name="name", bounds=IntegerBounds(0, 1))
    cond = ConditionTemplate(name="name", bounds=IntegerBounds(0, 1))

    template = MaterialTemplate("measurement template")
    spec = MaterialSpec("A spec", template=template,
                        properties=[PropertyAndConditions(
                            property=Property("name", template=prop, value=NominalInteger(1)),
                            conditions=[
                                Condition("name", template=cond, value=NominalInteger(1))
                            ]
                        )])

    assert template in spec.all_dependences()
    assert cond in spec.all_dependences()
    assert prop in spec.all_dependences()
