"""Tests of the process spec object."""
import pytest

from taurus.json import dumps, loads
from taurus.entity.attribute.property_and_conditions import PropertyAndConditions
from taurus.entity.object.process_spec import ProcessSpec
from taurus.entity.object.material_spec import MaterialSpec
from taurus.entity.object.ingredient_spec import IngredientSpec
from taurus.entity.attribute.property import Property
from taurus.entity.attribute.parameter import Parameter
from taurus.entity.value.discrete_categorical import DiscreteCategorical
from taurus.entity.value.nominal_real import NominalReal


process_spec = ProcessSpec(
    name="test process", parameters=[Parameter(name="test parameter", value=NominalReal(1.0, "N"))]
)


def test_material_spec():
    """Test that Process/Material Spec link survives serialization."""
    # Create a ProcessSpec
    proc_spec = ProcessSpec(name="a process spec", tags=["tag1", "tag2"])

    # Create MaterialSpec without a ProcessSpec
    prop = Property(
        name="The material is a solid", value=DiscreteCategorical(probabilities="solid")
    )
    mat_spec = MaterialSpec(name="a material spec", properties=PropertyAndConditions(prop))
    assert (
        mat_spec.process is None
    ), "MaterialSpec should be initialized with no ProcessSpec, by default"

    # Assign a ProcessSpec to mat_spec, first ensuring that the type is enforced
    with pytest.raises(TypeError):
        mat_spec.process = 17
    mat_spec.process = proc_spec

    # Assert circular links
    assert dumps(proc_spec.output_material.process) == dumps(
        proc_spec
    ), "ProcessSpec should link to MaterialSpec that links back to itself"

    assert dumps(mat_spec.process.output_material) == dumps(
        mat_spec
    ), "MaterialSpec should link to ProcessSpec that links back to itself"

    # Make copies of both specs
    mat_spec_copy = loads(dumps(mat_spec))
    proc_spec_copy = loads(dumps(proc_spec))

    assert (
        proc_spec_copy.output_material == mat_spec
    ), "Serialization should preserve link from ProcessSpec to MaterialSpec"

    assert (
        mat_spec_copy.process == proc_spec
    ), "Serialization should preserve link from MaterialSpec to ProcessSpec"


def test_ingredient_spec():
    """Tests that a process can house an ingredient, and that pairing survives serialization."""
    # Create a ProcessSpec
    proc_spec = ProcessSpec(name="a process spec", tags=["tag1", "tag2"])
    IngredientSpec(name="Input", material=MaterialSpec(name="Raw"), process=proc_spec)

    # Make copies of both specs
    proc_spec_copy = loads(dumps(proc_spec))

    assert proc_spec_copy == proc_spec, "Full structure wasn't preserved across serialization"


def test_creating_process_run():
    """Test creating a process run from a process spec."""

    process = process_spec()  # inherit default attributes from spec
    assert process.name == process_spec.name
    assert process.spec is process_spec
    for spec_pram, run_param in zip(process.parameters, process_spec.parameters):
        assert spec_pram == run_param
        assert spec_pram is not run_param

    process = process_spec(name="other name")  # change default values
    assert process.name == "other name"
