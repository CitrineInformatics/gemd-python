"""Tests of the process spec object."""
import pytest

from gemd.json import dumps, loads
from gemd.entity.attribute.property_and_conditions import PropertyAndConditions
from gemd.entity.object.process_spec import ProcessSpec
from gemd.entity.object.material_spec import MaterialSpec
from gemd.entity.object.ingredient_spec import IngredientSpec
from gemd.entity.attribute.property import Property
from gemd.entity.value.discrete_categorical import DiscreteCategorical


def test_material_spec():
    """Test that Process/Material Spec link survives serialization."""
    # Create a ProcessSpec
    proc_spec = ProcessSpec(name="a process spec", tags=["tag1", "tag2"])

    # Create MaterialSpec without a ProcessSpec
    prop = Property(
        name="The material is a solid",
        value=DiscreteCategorical(probabilities="solid")
    )
    mat_spec = MaterialSpec(name="a material spec", properties=PropertyAndConditions(prop))
    assert mat_spec.process is None, \
        "MaterialSpec should be initialized with no ProcessSpec, by default"

    # Assign a ProcessSpec to mat_spec, first ensuring that the type is enforced
    with pytest.raises(TypeError):
        mat_spec.process = 17
    mat_spec.process = proc_spec

    # Assert circular links
    assert dumps(proc_spec.output_material.process) == dumps(proc_spec), \
        "ProcessSpec should link to MaterialSpec that links back to itself"

    assert dumps(mat_spec.process.output_material) == dumps(mat_spec), \
        "MaterialSpec should link to ProcessSpec that links back to itself"

    # Make copies of both specs
    mat_spec_copy = loads(dumps(mat_spec))
    proc_spec_copy = loads(dumps(proc_spec))

    assert proc_spec_copy.output_material == mat_spec, \
        "Serialization should preserve link from ProcessSpec to MaterialSpec"

    assert mat_spec_copy.process == proc_spec, \
        "Serialization should preserve link from MaterialSpec to ProcessSpec"


def test_ingredient_spec():
    """Tests that a process can house an ingredient, and that pairing survives serialization."""
    # Create a ProcessSpec
    proc_spec = ProcessSpec(name="a process spec", tags=["tag1", "tag2"])
    IngredientSpec(name='Input', material=MaterialSpec(name='Raw'), process=proc_spec)

    # Make copies of both specs
    proc_spec_copy = loads(dumps(proc_spec))

    assert proc_spec_copy == proc_spec, "Full structure wasn't preserved across serialization"
