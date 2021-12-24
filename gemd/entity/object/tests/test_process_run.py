"""Tests of the process run object."""
import pytest
from uuid import uuid4
from copy import deepcopy

from gemd.json import dumps, loads
from gemd.entity.attribute import Condition
from gemd.entity.object import ProcessRun, ProcessSpec, IngredientRun, MaterialRun
from gemd.entity.template import ProcessTemplate
from gemd.entity.link_by_uid import LinkByUID
from gemd.util import flatten


def test_process_spec():
    """Tests that the Process Spec/Run connection persists when serializing."""
    # Create the ProcessSpec
    condition1 = Condition(name="a condition on the process in general")
    spec = ProcessSpec("Spec", conditions=condition1)

    # Create the ProcessRun with a link to the ProcessSpec from above
    condition2 = Condition(name="a condition on this process run in particular")
    process = ProcessRun("Run", conditions=condition2, spec=spec)

    copy_process = loads(dumps(process))
    assert dumps(copy_process.spec) == dumps(spec), \
        "Process spec should be preserved through serialization"


def test_ingredient_run():
    """Tests that a process can house an ingredient, and that pairing survives serialization."""
    # Create a ProcessSpec
    proc_run = ProcessRun(name="a process spec", tags=["tag1", "tag2"])
    ingred_run = IngredientRun(material=MaterialRun(name='Raw'), process=proc_run)

    # Make copies of both specs
    proc_run_copy = loads(dumps(proc_run))

    assert proc_run_copy == proc_run, "Full structure wasn't preserved across serialization"

    assert 'process' in repr(ingred_run)
    assert 'ingredients' in repr(proc_run)


def test_invalid_assignment():
    """Invalid assignments to `spec` throw a TypeError."""
    with pytest.raises(TypeError):
        ProcessRun("name", spec=[ProcessSpec("spec")])
    with pytest.raises(TypeError):
        ProcessRun()  # Name is required


def test_template_access():
    """A process run's template should be equal to its spec's template."""
    template = ProcessTemplate("process template", uids={'id': str(uuid4())})
    spec = ProcessSpec("A spec", uids={'id': str(uuid4())}, template=template)
    proc = ProcessRun("A run", uids={'id': str(uuid4())}, spec=spec)
    assert proc.template == template

    proc.spec = LinkByUID.from_entity(spec)
    assert proc.template is None


def test_equality():
    """Test that equality check works as expected."""
    spec = ProcessSpec("A spec", tags=["a tag"])
    run1 = ProcessRun("A process", spec=spec)

    run2 = deepcopy(run1)
    assert run1 == run2, "Copy somehow failed"
    IngredientRun(process=run2)
    assert run1 != run2

    run3 = deepcopy(run2)
    assert run3 == run2, "Copy somehow failed"
    run3.ingredients[0].tags.append('A tag')
    assert run3 != run2

    run4 = next(x for x in flatten(run3, 'test-scope') if isinstance(x, ProcessRun))
    assert run4 == run3, "Flattening removes measurement references, but that's okay"
