"""Tests of entity utils."""
import pytest

from taurus.entity.util import make_instance, complete_material_history
from taurus.entity.attribute.condition import Condition
from taurus.entity.attribute.property import Property
from taurus.entity.link_by_uid import LinkByUID
from taurus.entity.object.ingredient_spec import IngredientSpec
from taurus.entity.object.ingredient_run import IngredientRun
from taurus.entity.object.material_spec import MaterialSpec
from taurus.entity.object.material_run import MaterialRun
from taurus.entity.object.measurement_spec import MeasurementSpec
from taurus.entity.object.measurement_run import MeasurementRun
from taurus.entity.object.process_spec import ProcessSpec
from taurus.entity.object.process_run import ProcessRun
from taurus.entity.value.discrete_categorical import DiscreteCategorical
from taurus.entity.value.nominal_real import NominalReal
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


def test_serialized_history():
    """Test the serialization of a complete material history."""
    # Create several runs and specs linked together
    buy_spec = LinkByUID("id", "pr723")
    cookie_dough_spec = MaterialSpec("cookie dough spec", process=buy_spec)
    buy_cookie_dough = ProcessRun("Buy cookie dough", uids={'id': '32283'}, spec=buy_spec)
    cookie_dough = MaterialRun("cookie dough", process=buy_cookie_dough, spec=cookie_dough_spec)
    bake = ProcessRun("bake cookie dough", conditions=[
        Condition("oven temp", origin='measured', value=NominalReal(357, 'degF'))])
    IngredientRun(name="all of the cookie dough", material=cookie_dough,
                  process=bake, number_fraction=NominalReal(1, ''))
    cookie = MaterialRun("cookie", process=bake, tags=["chocolate chip", "drop"])
    MeasurementRun("taste", material=cookie, properties=[
        Property("taste", value=DiscreteCategorical("scrumptious"))])

    cookie_history = complete_material_history(cookie)
    # There are 7 entities in the serialized list: cookie dough (spec & run), buy cookie dough,
    # cookie dough ingredient, bake cookie dough, cookie, taste
    assert len(cookie_history) == 7
    for entity in cookie_history:
        assert len(entity['uids']) > 0, "Serializing material history should assign uids."

    # Check that the measurement points to the material
    taste_dict = next(x for x in cookie_history if x.get('type') == 'measurement_run')
    cookie_dict = next(x for x in cookie_history if x.get('name') == 'cookie')
    scope = taste_dict.get('material').get('scope')
    assert taste_dict.get('material').get('id') == cookie_dict.get('uids').get(scope)

    # Check that both the material spec and the process run point to the same process spec.
    # Because that spec was initially a LinkByUID, this also tests the methods ability to
    # serialize a LinkByUID.
    cookie_dough_spec_dict = next(x for x in cookie_history if x.get('type') == 'material_spec')
    buy_cookie_dough_dict = next(x for x in cookie_history if x.get('name') == 'Buy cookie dough')
    assert cookie_dough_spec_dict.get('process') == buy_spec.as_dict()
    assert buy_cookie_dough_dict.get('spec') == buy_spec.as_dict()

    from taurus.util.impl import substitute_objects
    substitute_objects(cookie_history, {})


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
