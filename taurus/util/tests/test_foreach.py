from taurus.entity.object import ProcessRun, MaterialRun, IngredientRun
from taurus.util.impl import recursive_foreach


def test_recursive_foreach():
    """Test that recursive foreach will actually walk through a material history"""
    mat_run = MaterialRun("foo")
    process_run = ProcessRun("bar")
    ingredient_run = IngredientRun(process=process_run, material=mat_run, name="foobar")
    output = MaterialRun(process=process_run)

    types = []
    recursive_foreach(output, lambda x: types.append(x.typ))

    assert sorted(types) == ["ingredient_run", "material_run", "material_run", "process_run"]
