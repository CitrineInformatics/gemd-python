from gemd.entity.attribute.property import Property
from gemd.entity.bounds.real_bounds import RealBounds
from gemd.entity.object import ProcessRun, MaterialRun, IngredientRun, MeasurementRun
from gemd.entity.template.property_template import PropertyTemplate
from gemd.entity.value.nominal_real import NominalReal
from gemd.util.impl import recursive_foreach


def test_recursive_foreach():
    """Test that recursive foreach will actually walk through a material history."""
    mat_run = MaterialRun("foo")
    process_run = ProcessRun("bar")
    IngredientRun(process=process_run, material=mat_run)
    output = MaterialRun("material", process=process_run)

    # property templates are trickier than templates because they are referenced in attributes
    template = PropertyTemplate("prop", bounds=RealBounds(0, 1, ""))
    prop = Property("prop", value=NominalReal(1.0, ""), template=template)
    MeasurementRun("check", material=output, properties=prop)

    types = []
    recursive_foreach(output, lambda x: types.append(x.typ))

    expected = ["ingredient_run",
                "material_run", "material_run",
                "process_run",
                "measurement_run",
                "property_template"
                ]
    assert sorted(types) == sorted(expected)


def test_more_iterable_types():
    """Verify recursive_foreach behaves for additional iterable types."""
    obj = MaterialRun("foo", tags=["1", "2", "3"])

    assert "1" in obj.tags
    recursive_foreach({obj}, lambda x: x.tags.remove("1"))
    assert "1" not in obj.tags

    dct = {obj: obj}
    assert "2" in obj.tags
    recursive_foreach(dct.keys(), lambda x: x.tags.remove("2"))
    assert "2" not in obj.tags

    assert "3" in obj.tags
    recursive_foreach(dct.values(), lambda x: x.tags.remove("3"))
    assert "3" not in obj.tags
