"""Tests of entity utils."""
import pytest

from taurus.entity.util import make_instance
from taurus.entity.object.ingredient_spec import IngredientSpec
from taurus.entity.object.ingredient_run import IngredientRun
from taurus.entity.object.material_spec import MaterialSpec
from taurus.entity.object.material_run import MaterialRun
from taurus.entity.object.measurement_spec import MeasurementSpec
from taurus.entity.object.measurement_run import MeasurementRun
from taurus.entity.object.process_spec import ProcessSpec
from taurus.entity.object.process_run import ProcessRun
from taurus.entity.attribute.condition import Condition
from taurus.entity.value.uniform_real import UniformReal


def test_make_instance():
    """Build up several linked objects and test their properties."""
    msr_spec = MeasurementSpec()
    assert isinstance(make_instance(msr_spec), MeasurementRun)

    mat_spec = MaterialSpec(name='Mat name')
    mat_spec.process = ProcessSpec(name='Pro name')
    IngredientSpec(name='Ing label', process=mat_spec.process)
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


def test_invalid_instance():
    """Calling make_instance on a non-spec should throw a TypeError."""
    not_specs = [MeasurementRun("meas"), Condition("cond"), UniformReal(0, 1, ''), 'foo', 10]
    for not_spec in not_specs:
        with pytest.raises(TypeError):
            make_instance(not_spec)


def test_circular_crawl():
    """Test that make_instance can handle a circular set of linked objects."""
    proc = ProcessSpec("process name")
    mat = MaterialSpec("material name", process=proc)
    IngredientSpec(name="ingredient name", material=mat, process=proc)
    mat_run = make_instance(mat)
    assert mat_run == mat_run.process.ingredients[0].material
