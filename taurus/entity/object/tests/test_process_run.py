"""Tests of the process run object."""
from taurus.client.json_encoder import dumps, loads
from taurus.entity.object.process_run import ProcessRun
from taurus.entity.object.process_spec import ProcessSpec
from taurus.entity.attribute.condition import Condition
from taurus.entity.object.ingredient_run import IngredientRun
from taurus.entity.object.material_run import MaterialRun


def test_process_spec():
    """Tests that the Process Spec/Run connection persists when serializing."""
    # Create the ProcessSpec
    condition1 = Condition(name="a condition on the process in general")
    spec = ProcessSpec(conditions=condition1)

    # Create the ProcessRun with a link to the ProcessSpec from above
    condition2 = Condition(name="a condition on this process run in particular")
    process = ProcessRun(conditions=condition2, spec=spec)

    copy_process = loads(dumps(process))
    assert dumps(copy_process.spec) == dumps(spec), \
        "Process spec should be preserved through serialization"


def test_ingredient_run():
    """Tests that a process can house an ingredient, and that pairing survives serialization."""
    # Create a ProcessSpec
    proc_run = ProcessRun(
        name="a process spec",
        tags=["tag1", "tag2"],
        ingredients=IngredientRun(unique_label='Input', material=MaterialRun(name='Raw'))
    )

    # Make copies of both specs
    proc_run_copy = loads(dumps(proc_run))

    assert proc_run_copy == proc_run, "Full structure wasn't preserved across serialization"
