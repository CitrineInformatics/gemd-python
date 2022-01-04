"""Tests of the material spec object."""
import pytest

from gemd.entity.attribute import PropertyAndConditions, Property, Condition
from gemd.entity.bounds import IntegerBounds
from gemd.entity.object import ProcessSpec, MaterialSpec
from gemd.entity.template import MaterialTemplate, PropertyTemplate, ConditionTemplate
from gemd.entity.value import NominalInteger
from gemd.entity.bounds_validation import validation_level, WarningLevel


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


def test_mat_spec_properties(caplog):
    """Make sure template validations and level controls behave as expected."""
    prop_tmpl = PropertyTemplate("Name", bounds=IntegerBounds(0, 2))
    cond_tmpl = ConditionTemplate("Name", bounds=IntegerBounds(0, 2))
    mat_tmpl = MaterialTemplate("Material Template", properties=[[prop_tmpl, IntegerBounds(0, 1)]])
    mat_spec = MaterialSpec("Material Spec", template=mat_tmpl)
    good_prop = PropertyAndConditions(
        property=Property("Name", value=NominalInteger(1), template=prop_tmpl),
        conditions=[Condition("Name", value=NominalInteger(1), template=cond_tmpl)]
    )
    bad_prop = PropertyAndConditions(
        property=Property("Name", value=NominalInteger(2), template=prop_tmpl),
        conditions=[Condition("Name", value=NominalInteger(1), template=cond_tmpl)]
    )
    bad_cond = PropertyAndConditions(  # This will pass since we don't have a condition constraint
        property=Property("Name", value=NominalInteger(1), template=prop_tmpl),
        conditions=[Condition("Name", value=NominalInteger(2), template=cond_tmpl)]
    )
    with validation_level(WarningLevel.IGNORE):
        mat_spec.properties.append(good_prop)
        assert len(caplog.records) == 0, "Warning encountered on IGNORE"
        mat_spec.properties.append(bad_prop)
        assert len(caplog.records) == 0, "Warning encountered on IGNORE"
        mat_spec.properties.append(bad_cond)
        assert len(caplog.records) == 0, "Warning encountered on IGNORE"
    with validation_level(WarningLevel.WARNING):
        mat_spec.properties.append(good_prop)
        assert len(caplog.records) == 0, "Warning encountered on Good value"
        mat_spec.properties.append(bad_prop)
        assert len(caplog.records) == 1, "No warning encountered on Bad Value"
        mat_spec.properties.append(bad_cond)
        assert len(caplog.records) == 1, "Warning encountered on Bad condition"
    with validation_level(WarningLevel.FATAL):
        mat_spec.properties.append(good_prop)  # This is fine
        with pytest.raises(ValueError):
            mat_spec.properties.append(bad_prop)
        mat_spec.properties.append(bad_cond)  # This should probably not be fine


def test_dependencies():
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

    assert template in spec.all_dependencies()
    assert cond in spec.all_dependencies()
    assert prop in spec.all_dependencies()
