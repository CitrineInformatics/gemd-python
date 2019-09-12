"""Tests of entity utils."""
from taurus.entity.util import make_instance

from taurus.entity.object.ingredient_spec import IngredientSpec
from taurus.entity.object.ingredient_run import IngredientRun
from taurus.entity.object.material_spec import MaterialSpec
from taurus.entity.object.material_run import MaterialRun
from taurus.entity.object.measurement_spec import MeasurementSpec
from taurus.entity.object.measurement_run import MeasurementRun
from taurus.entity.object.process_spec import ProcessSpec
from taurus.entity.object.process_run import ProcessRun


def test_make_instance():
    """Build up several linked objects and test their properties."""
    msr_spec = MeasurementSpec()
    assert isinstance(make_instance(msr_spec), MeasurementRun)

    mat_spec = MaterialSpec(name='Mat name')
    mat_spec.process = ProcessSpec(name='Pro name')
    IngredientSpec(unique_label='Ing label', process=mat_spec.process)
    mat_spec.process.ingredients[0].material = MaterialSpec(name='Baby mat name')

    mat_run = make_instance(mat_spec)
    assert isinstance(mat_run, MaterialRun)
    assert isinstance(mat_run.process, ProcessRun)
    assert isinstance(mat_run.process.ingredients[0], IngredientRun)
    assert isinstance(mat_run.process.ingredients[0].material, MaterialRun)

    assert mat_run.process.spec == mat_run.spec.process
    ingredient = mat_run.process.ingredients[0]
    assert ingredient.spec == mat_run.spec.process.ingredients[0]
    assert ingredient.material.spec == mat_run.spec.process.ingredients[0].material
