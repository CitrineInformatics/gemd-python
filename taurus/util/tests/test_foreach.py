from taurus.entity.attribute.property import Property
from taurus.entity.bounds.real_bounds import RealBounds
from taurus.entity.object import ProcessRun, MaterialRun, IngredientRun, MeasurementRun
from taurus.entity.template.property_template import PropertyTemplate
from taurus.entity.value.nominal_real import NominalReal
from taurus.util.impl import recursive_foreach


def test_recursive_foreach():
    """Test that recursive foreach will actually walk through a material history."""
    mat_run = MaterialRun("foo")
    process_run = ProcessRun("bar")
    IngredientRun(process=process_run, material=mat_run, name="foobar")
    output = MaterialRun(process=process_run)

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
