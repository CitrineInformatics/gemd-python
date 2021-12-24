from gemd.entity.bounds.categorical_bounds import CategoricalBounds
from gemd.entity.object import ProcessSpec, MaterialSpec, IngredientSpec, ProcessRun, \
    MaterialRun, IngredientRun
from gemd.entity.template.condition_template import ConditionTemplate
from gemd.entity.template.process_template import ProcessTemplate
from gemd.entity.attribute.condition import Condition
from gemd.entity.value.nominal_categorical import NominalCategorical
from gemd.util import flatten, recursive_flatmap

import pytest


def test_flatten_bounds():
    """Test that flatten works when the objects contain other objects."""
    bounds = CategoricalBounds(categories=["foo", "bar"])
    template = ProcessTemplate(
        "spam",
        conditions=[(ConditionTemplate(name="eggs", bounds=bounds), bounds)]
    )
    spec = ProcessSpec(name="spec", template=template)

    flat = flatten(spec, 'test-scope')
    # 3 objects: 1 Process Template, 1 Condition Template and 1 Process Spec
    assert len(flat) == 3, "Expected 3 flattened objects"


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

    assert len(flatten(procured, 'test-scope')) == 2
    assert 'test-scope' in procured.uids
    assert len(flatten(input, 'test-scope')) == 2
    assert len(flatten(ingredient, 'test-scope')) == 4
    assert len(flatten(transform, 'test-scope')) == 4

    assert len(flatten(procured_run, 'test-scope')) == 4
    assert len(flatten(input_run, 'test-scope')) == 4
    assert len(flatten(ingredient_run, 'test-scope')) == 8
    assert len(flatten(transform_run, 'test-scope')) == 8


def test_default_scope():
    """Test flatten exceptions around providing a scope."""
    ps_one = ProcessSpec(name="one")

    with pytest.raises(ValueError):
        flatten(ps_one)

    pr_one = ProcessRun(name="one", uids={'my': 'outer'}, spec=ps_one)

    with pytest.raises(ValueError):
        flatten(pr_one)

    ps_one.uids['my'] = 'id'
    assert len(flatten(pr_one)) == 2

    two = ProcessRun(name="two", spec=ProcessSpec(name="two"))
    assert len(flatten(two, scope="my")) == 2


def test_flatmap_unidirectional_ordering():
    """Test that the unidirecitonal setting is obeyed."""
    # The writeable link is ingredient -> process, not process -> ingredients
    proc = ProcessRun(name="foo")
    IngredientRun(notes="bar", process=proc)

    assert len(recursive_flatmap(proc, lambda x: [x], unidirectional=False)) == 2
    assert len(recursive_flatmap(proc, lambda x: [x], unidirectional=True)) == 1


def test_repeated_objects():
    """Test that objects aren't double counted."""
    ct = ConditionTemplate(name="color",
                           bounds=CategoricalBounds(categories=["black", "white"]))
    pt = ProcessTemplate(name="painting", conditions=[ct])
    ps = ProcessSpec(name='painting',
                     template=pt,
                     conditions=Condition(name='Paint color',
                                          value=NominalCategorical("black"),
                                          template=ct
                                          )
                     )
    assert len(recursive_flatmap(ps, lambda x: [x])) == 3


def test_recursive_flatmap_maintains_order():
    """Test flatmap preserves order in lists."""
    p1 = ProcessSpec(name="one")
    p2 = ProcessSpec(name="two")
    orig = [p1, p2]
    assert [x.name for x in orig] == recursive_flatmap(orig, lambda x: [x.name])


def test_more_iterable_types():
    """Verify recursive_flatmap behaves for additional iterable types."""
    obj = MaterialRun("foo", tags=["1", "2", "3"])

    assert "1" in obj.tags
    res = recursive_flatmap({obj}, lambda x: [x.tags.pop(0)])
    assert "1" in res
    assert "1" not in obj.tags

    dct = {obj: obj}
    assert "2" in obj.tags
    res = recursive_flatmap(dct.keys(), lambda x: [x.tags.pop(0)])
    assert "2" in res
    assert "2" not in obj.tags

    assert "3" in obj.tags
    res = recursive_flatmap(dct.values(), lambda x: [x.tags.pop(0)])
    assert "3" in res
    assert "3" not in obj.tags
