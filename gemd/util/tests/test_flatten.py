from gemd.entity.bounds.categorical_bounds import CategoricalBounds
from gemd.entity.object import ProcessSpec, MaterialSpec, IngredientSpec, ProcessRun, \
    MaterialRun, IngredientRun
from gemd.entity.template.condition_template import ConditionTemplate
from gemd.entity.template.process_template import ProcessTemplate
from gemd.util import flatten, recursive_flatmap


def test_flatten_bounds():
    """Test that flatten works when the objects contain other objects."""
    bounds = CategoricalBounds(categories=["foo", "bar"])
    template = ProcessTemplate(
        "spam",
        conditions=[(ConditionTemplate(name="eggs", bounds=bounds), bounds)]
    )
    spec = ProcessSpec(name="spec", template=template)

    flat = flatten(spec, 'test-scope')
    assert len(flat) == 2, "Expected 2 flattened objects"


def test_flatten_empty_history():
    """Test that flatten works when the objects are empty and go through a whole history."""
    procured = ProcessSpec(name="procured")
    input = MaterialSpec(name="foo", process=procured)
    transform = ProcessSpec(name="transformed")
    ingredient = IngredientSpec(name="input", material=input, process=transform)

    procured_run = ProcessRun(name="procured", spec=procured)
    input_run = MaterialRun(name="foo", process=procured_run, spec=input)
    transform_run = ProcessRun(name="transformed", spec=transform)
    ingredient_run = IngredientRun(material=input_run, process=transform_run, spec=ingredient)

    assert len(flatten(procured, 'test-scope')) == 1
    assert 'test-scope' in procured.uids
    assert len(flatten(input, 'test-scope')) == 1
    assert len(flatten(ingredient, 'test-scope')) == 3
    assert len(flatten(transform, 'test-scope')) == 3

    assert len(flatten(procured_run, 'test-scope')) == 3
    assert len(flatten(input_run, 'test-scope')) == 3
    assert len(flatten(ingredient_run, 'test-scope')) == 7
    assert len(flatten(transform_run, 'test-scope')) == 7


def test_flatmap_unidirectional_ordering():
    """Test that the unidirecitonal setting is obeyed."""
    # The writeable link is ingredient -> process, not process -> ingredients
    proc = ProcessRun(name="foo")
    IngredientRun(notes="bar", process=proc)

    assert len(recursive_flatmap(proc, lambda x: [x], unidirectional=False)) == 2
    assert len(recursive_flatmap(proc, lambda x: [x], unidirectional=True)) == 0
