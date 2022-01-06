"""Tests of the process spec object."""
import pytest
from copy import deepcopy

from gemd.json import dumps, loads
from gemd.entity.attribute import PropertyAndConditions, Property
from gemd.entity.object import ProcessSpec, MaterialSpec, IngredientSpec
from gemd.entity.value import DiscreteCategorical
from gemd.util import flatten


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


def test_invalid_assignment():
    """Omitting a name throws a TypeError."""
    with pytest.raises(TypeError):
        ProcessSpec()  # Name is required


def test_equality():
    """Test that equality check works as expected."""
    spec1 = ProcessSpec("A spec")
    spec2 = ProcessSpec("A spec", tags=["a tag"])

    assert spec1 != spec2
    spec3 = deepcopy(spec1)
    assert spec1 == spec3, "Copy somehow failed"
    IngredientSpec("An ingredient", process=spec3)
    assert spec1 != spec3

    spec4 = deepcopy(spec3)
    assert spec4 == spec3, "Copy somehow failed"
    spec4.ingredients[0].tags.append('A tag')
    assert spec4 != spec3

    spec5 = next(x for x in flatten(spec4, 'test-scope') if isinstance(x, ProcessSpec))
    assert spec5 == spec4, "Flattening removes measurement references, but that's okay"


def test_template_check_generator():
    """Verify that the generator throws exceptions."""
    spec1 = ProcessSpec("A spec")
    with pytest.raises(ValueError):  # Can't find class
        spec1._generate_template_check(validate=lambda x, y: True)

    with pytest.raises(ValueError):  # Can't find attribute
        spec1._generate_template_check(validate=ProcessSpec.name.fget)
