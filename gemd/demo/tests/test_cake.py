"""Test cake demo."""
from gemd.entity.object.material_spec import MaterialSpec
from gemd.entity.object.material_run import MaterialRun
from gemd.entity.object.process_run import ProcessRun
from gemd.entity.object.process_spec import ProcessSpec
from gemd.entity.object.measurement_spec import MeasurementSpec
from gemd.entity.object.measurement_run import MeasurementRun
from gemd.entity.object.ingredient_spec import IngredientSpec
from gemd.entity.object.ingredient_run import IngredientRun

from gemd.json import dumps, loads
from gemd.demo.cake import make_cake, import_toothpick_picture
from gemd.util import recursive_foreach
from gemd.entity.util import complete_material_history


def test_cake():
    """Create cake, serialize, deserialize."""
    cake = make_cake()

    def test_for_loss(obj):
        assert(obj == loads(dumps(obj)))
    recursive_foreach(cake, test_for_loss)

    # And verify equality was working in the first place
    cake2 = loads(dumps(cake))
    cake2.name = "It's a trap!"
    assert(cake2 != cake)
    cake2.name = cake.name
    assert(cake == cake2)
    cake2.uids['new'] = "It's a trap!"
    assert(cake2 != cake)

    # Check that all the objects show up
    tot_count = 0

    def increment(dummy):
        nonlocal tot_count
        tot_count += 1

    recursive_foreach(cake, increment)
    assert tot_count == 131

    # And make sure nothing was lost
    tot_count = 0
    recursive_foreach(loads(dumps(complete_material_history(cake))), increment)
    assert tot_count == 131

    # Check that no UIDs collide
    uid_seen = dict()

    def check_ids(obj):
        nonlocal uid_seen
        for scope in obj.uids:
            lbl = '{}::{}'.format(scope, obj.uids[scope])
            if lbl in uid_seen:
                assert uid_seen[lbl] == id(obj)
            uid_seen[lbl] = id(obj)
    recursive_foreach(cake, check_ids)

    queue = [cake]
    seen = set()
    while queue:
        obj = queue.pop()
        if obj in seen:
            continue

        seen.add(obj)

        if isinstance(obj, MaterialSpec):
            if obj.process is not None:
                queue.append(obj.process)
                assert obj.process.output_material == obj
        elif isinstance(obj, MaterialRun):
            if obj.process is not None:
                queue.append(obj.process)
                assert obj.process.output_material == obj
            if obj.measurements:
                queue.extend(obj.measurements)
                for msr in obj.measurements:
                    assert msr.material == obj
            if obj.spec is not None:
                queue.append(obj.spec)
                if obj.process is not None:
                    assert obj.spec.process == obj.process.spec
        elif isinstance(obj, ProcessRun):
            if obj.ingredients:
                queue.extend(obj.ingredients)
            if obj.output_material is not None:
                queue.append(obj.output_material)
                assert obj.output_material.process == obj
                if obj.spec is not None:
                    assert obj.spec.output_material == obj.output_material.spec
        elif isinstance(obj, ProcessSpec):
            if obj.ingredients:
                queue.extend(obj.ingredients)
            if obj.output_material is not None:
                queue.append(obj.output_material)
                assert obj.output_material.process == obj
        elif isinstance(obj, MeasurementSpec):
            pass  # Doesn't link
        elif isinstance(obj, MeasurementRun):
            if obj.spec:
                queue.append(obj.spec)
        elif isinstance(obj, IngredientSpec):
            if obj.material:
                queue.append(obj.material)
        elif isinstance(obj, IngredientRun):
            if obj.spec:
                queue.append(obj.spec)
                if obj.material and isinstance(obj.material, MaterialRun):
                    assert obj.spec.material == obj.material.spec
            if obj.material:
                queue.append(obj.material)


def test_import():
    """Make sure picture import runs."""
    import_toothpick_picture()
