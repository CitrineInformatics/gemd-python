"""Test of the material run object."""
import pytest
import json
from uuid import uuid4
from copy import deepcopy

from taurus.client.json_encoder import loads, dumps
from taurus.entity.attribute.property_and_conditions import PropertyAndConditions
from taurus.entity.object import MaterialRun, ProcessRun, MaterialSpec
from taurus.entity.template.material_template import MaterialTemplate
from taurus.entity.attribute.property import Property
from taurus.entity.value.nominal_real import NominalReal
from taurus.entity.link_by_uid import LinkByUID


def test_material_run():
    """
    Test the ability to create a MaterialRun that is linked to a MaterialSpec.

    Make sure all enumerated values are respected, and check consistency after
    serializing and deserializing.
    """
    # Define a property, and make sure that an inappropriate value for origin throws ValueError
    with pytest.raises(ValueError):
        prop = Property(name="A property", origin="bad origin", value=NominalReal(17, units=''))

    # Create a MaterialSpec with a property
    prop = Property(name="A property", origin="specified", value=NominalReal(17, units=''))
    mat_spec = MaterialSpec(
        name="a specification for a material",
        properties=PropertyAndConditions(prop),
        notes="Funny lookin'"
    )

    # Make sure that when property is serialized, origin (an enumeration) is serialized as a string
    copy_prop = json.loads(dumps(mat_spec))
    copy_origin = copy_prop[0][0]["properties"][0]['property']['origin']
    assert isinstance(copy_origin, str)

    # Create a MaterialRun, and make sure an inappropriate value for sample_type throws ValueError
    with pytest.raises(ValueError):
        mat = MaterialRun(spec=mat_spec, sample_type="imaginary")
    mat = MaterialRun(spec=mat_spec, sample_type="virtual")

    # ensure that serialization does not change the MaterialRun
    copy = loads(dumps(mat))
    assert dumps(copy) == dumps(mat), \
        "Material run is modified by serialization or deserialization"


def test_process_run():
    """Test that a process run can house a material, and that it survives serde."""
    process_run = ProcessRun("Bake a cake", uids={'My_ID': str(17)})
    material_run = MaterialRun("A cake", process=process_run)

    # Check that a bi-directional link is established
    assert material_run.process == process_run
    assert process_run.output_material == material_run

    print("Before")
    copy_material = loads(dumps(material_run))
    print("After")
    print(copy_material)
    # print(dumps(material_run, indent=2))
    # print(copy_material.process)
    # print(dumps(copy_material, indent=2))
    assert dumps(copy_material) == dumps(material_run)

    assert 'output_material' in repr(process_run)
    assert 'process' in repr(material_run)


def test_process_id_link():
    """Test that a process run can house a LinkByUID object, and that it survives serde."""
    uid = str(uuid4())
    proc_link = LinkByUID(scope='id', id=uid)
    mat_run = MaterialRun("Another cake", process=proc_link)
    copy_material = loads(dumps(mat_run))
    assert dumps(copy_material) == dumps(mat_run)


def test_process_reassignment():
    """Test that a material can be assigned to a new process."""
    drying = ProcessRun("drying")
    welding = ProcessRun("welding")
    powder = MaterialRun("Powder", process=welding)

    assert powder.process == welding
    assert welding.output_material == powder

    powder.process = drying
    assert powder.process == drying
    assert drying.output_material == powder
    assert welding.output_material is None


def test_invalid_assignment():
    """Invalid assignments to `process` or `spec` throw a TypeError."""
    with pytest.raises(TypeError):
        MaterialRun(name=12)
    with pytest.raises(TypeError):
        MaterialRun("name", spec=ProcessRun("a process"))
    with pytest.raises(TypeError):
        MaterialRun("name", process=MaterialSpec("a spec"))


def test_template_access():
    """A material run's template should be equal to its spec's template."""
    template = MaterialTemplate("material template", uids={'id': str(uuid4())})
    spec = MaterialSpec("A spec", uids={'id': str(uuid4())}, template=template)
    mat = MaterialRun("A run", uids=['id', str(uuid4())], spec=spec)
    assert mat.template == template

    mat.spec = LinkByUID.from_entity(spec)
    assert mat.template is None


def test_build():
    """Test that build recreates the material."""
    spec = MaterialSpec("A spec",
                        properties=PropertyAndConditions(
                            property=Property("a property", value=NominalReal(3, ''))),
                        tags=["a tag"])
    mat = MaterialRun(name="a material", spec=spec)
    mat_dict = mat.as_dict()
    mat_dict['spec'] = mat.spec.as_dict()
    assert MaterialRun.build(mat_dict) == mat


def test_equality():
    """Test that equality check works as expected."""
    spec = MaterialSpec("A spec",
                        properties=PropertyAndConditions(
                            property=Property("a property", value=NominalReal(3, ''))),
                        tags=["a tag"])
    mat1 = MaterialRun("A material", spec=spec)
    mat2 = MaterialRun("A material", spec=spec, tags=["A tag"])
    assert mat1 == deepcopy(mat1)
    assert mat1 != mat2
    assert mat1 != "A material"
