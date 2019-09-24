"""Test cake demo."""
from taurus.entity.object.material_spec import MaterialSpec
from taurus.entity.object.material_run import MaterialRun
from taurus.entity.object.process_run import ProcessRun
from taurus.entity.object.process_spec import ProcessSpec
from taurus.entity.object.measurement_spec import MeasurementSpec
from taurus.entity.object.measurement_run import MeasurementRun
from taurus.entity.object.ingredient_spec import IngredientSpec
from taurus.entity.object.ingredient_run import IngredientRun

from taurus.client.json_encoder import dumps, loads
from taurus.demo.cake import make_cake


def test_cake():
    """Create cake, serialize, deserialize."""
    cake = make_cake()
    assert dumps(loads(dumps(cake)), indent=2) == dumps(cake, indent=2)

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
                if obj.material:
                    assert obj.spec.material == obj.material.spec
            if obj.material:
                queue.append(obj.material)
