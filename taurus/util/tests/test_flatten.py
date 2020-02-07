from taurus.entity.bounds.categorical_bounds import CategoricalBounds
from taurus.entity.object import ProcessSpec, MaterialSpec, IngredientSpec
from taurus.entity.template.condition_template import ConditionTemplate
from taurus.entity.template.process_template import ProcessTemplate
from taurus.util import flatten


def test_flatten_bounds():
    """Test that flatten works when the objects contain other objects"""

    bounds = CategoricalBounds(categories=["foo", "bar"])
    template = ProcessTemplate(
        "spam",
        conditions=[(ConditionTemplate(name="eggs", bounds=bounds), bounds)]
    )
    spec = ProcessSpec(name="spec", template=template)

    flat = flatten(spec)
    assert len(flat) == 2, "Expected 2 flattened objects"


def test_flatten_empty_history():
    """Test that flatten works when the objects are empty and go through a whole history"""
    procured = ProcessSpec(name="procured")
    input = MaterialSpec(name="foo", process=procured)
    transform = ProcessSpec(name="transformed")
    IngredientSpec(name="input", material=input, process=transform)

    assert len(flatten(procured)) == 1
    assert len(flatten(input)) == 2
    assert len(flatten(transform)) == 4
