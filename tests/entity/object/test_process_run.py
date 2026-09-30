"""Tests of the process run object."""

from copy import deepcopy
from uuid import uuid4

import pytest

from gemd.entity.attribute import Condition
from gemd.entity.link_by_uid import LinkByUID
from gemd.entity.object import IngredientRun, MaterialRun, ProcessRun, ProcessSpec
from gemd.entity.template import ProcessTemplate
from gemd.json import dumps, loads
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
    assert dumps(copy_process.spec) == dumps(spec), (
        "Process spec should be preserved through serialization"
    )


def test_ingredient_run():
    """Tests that a process can house an ingredient, and that pairing survives serialization."""
    # Create a ProcessSpec
    proc_run = ProcessRun(name="a process spec", tags=["tag1", "tag2"])
    ingred_run = IngredientRun(material=MaterialRun(name="Raw"), process=proc_run)

    # Make copies of both specs
    proc_run_copy = loads(dumps(proc_run))

    assert proc_run_copy == proc_run, "Full structure wasn't preserved across serialization"

    assert "process" in repr(ingred_run)
    assert "ingredients" in repr(proc_run)


def test_invalid_assignment():
    """Invalid assignments to `spec` throw a TypeError."""
    with pytest.raises(TypeError):
        ProcessRun("name", spec=[ProcessSpec("spec")])
    with pytest.raises(TypeError):
        ProcessRun()  # Name is required


def test_template_access():
    """A process run's template should be equal to its spec's template."""
    template = ProcessTemplate("process template", uids={"id": str(uuid4())})
    spec = ProcessSpec("A spec", uids={"id": str(uuid4())}, template=template)
    proc = ProcessRun("A run", uids={"id": str(uuid4())}, spec=spec)
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
    run3.ingredients[0].tags.append("A tag")
    assert run3 != run2

    run4 = next(x for x in flatten(run3, "test-scope") if isinstance(x, ProcessRun))
    assert run4 == run3, "Flattening removes measurement references, but that's okay"


def test_own_template():
    """A run's own template wins over its spec's template."""
    spec_template = ProcessTemplate("spec template", uids={"id": str(uuid4())})
    run_template = ProcessTemplate("run template", uids={"id": str(uuid4())})
    spec = ProcessSpec("A spec", uids={"id": str(uuid4())}, template=spec_template)

    assert ProcessRun("A run", template=run_template).template == run_template
    assert ProcessRun("A run", spec=spec).template == spec_template
    assert ProcessRun("A run", spec=spec, template=spec_template).template == spec_template
    assert ProcessRun("A run", spec=spec, template=run_template).template == run_template
    assert ProcessRun("A run").template is None

    with pytest.raises(TypeError):
        ProcessRun("A run", template=spec)

    run = ProcessRun("A run", uids={"id": str(uuid4())}, template=run_template)
    assert loads(dumps(run)).template == run_template


def test_own_template_bounds_check():
    """A run with a template and no spec checks its attributes against the template."""
    from gemd.entity.bounds import IntegerBounds
    from gemd.entity.bounds_validation import WarningLevel, validation_level
    from gemd.entity.template import ConditionTemplate
    from gemd.entity.value import NominalInteger

    cond_template = ConditionTemplate("cond", bounds=IntegerBounds(0, 10))
    template = ProcessTemplate("run template", conditions=[(cond_template, IntegerBounds(0, 5))])
    too_big = Condition("cond", template=cond_template, value=NominalInteger(7))

    with validation_level(WarningLevel.IGNORE):
        ProcessRun("A run", template=template, conditions=[too_big])
    with validation_level(WarningLevel.FATAL):
        ProcessRun("A run", conditions=[too_big])  # No template, so nothing to check
        with pytest.raises(ValueError):
            ProcessRun("A run", template=template, conditions=[too_big])
        run = ProcessRun("A run", template=template)
        with pytest.raises(ValueError):
            run.conditions.append(too_big)
