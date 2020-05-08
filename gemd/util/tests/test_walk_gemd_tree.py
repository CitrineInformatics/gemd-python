import pytest

from gemd.entity.object import ProcessSpec, MaterialSpec, IngredientSpec, ProcessRun, \
    MaterialRun, IngredientRun, MeasurementRun, MeasurementSpec


@pytest.fixture(scope="session")
def cake_gems():
    """A set of GEMD objects made from cake."""
    from gemd.util.impl import walk_gemd_tree
    from gemd.demo.cake import make_cake

    cake_material = make_cake(seed=42)
    cake_gems = walk_gemd_tree(cake_material)

    return cake_gems


def test_walk_gemd_tree_exception():
    """Test that value errors are raised when the input is invalid.

    Invalid inputs are non-MaterialRun objects
    """
    from gemd.util.impl import walk_gemd_tree

    with pytest.raises(ValueError):
        walk_gemd_tree(ProcessRun("process"))


def test_number_material_runs(cake_gems):
    """Tests that the number of material runs are correct."""
    material_runs = [gem for gem in cake_gems if isinstance(gem, MaterialRun)]

    assert len(material_runs) == 15


def test_number_material_specs(cake_gems):
    """Tests that the number of material specs are correct."""
    material_specs = [gem for gem in cake_gems if isinstance(gem, MaterialSpec)]

    assert len(material_specs) == 15


def test_number_material_templates(cake_gems):
    """Tests that the number of material templates are correct."""
    from gemd.entity.template.material_template import MaterialTemplate

    material_templates = [gem for gem in cake_gems if isinstance(gem, MaterialTemplate)]

    assert len(material_templates) == 4


def test_number_process_runs(cake_gems):
    """Tests that the number of process runs are correct."""
    process_runs = [gem for gem in cake_gems if isinstance(gem, ProcessRun)]

    assert len(process_runs) == 15


def test_number_process_specs(cake_gems):
    """Tests that the number of process specs are correct."""
    process_specs = [gem for gem in cake_gems if isinstance(gem, ProcessSpec)]

    assert len(process_specs) == 15


def test_number_process_templates(cake_gems):
    """Tests that the number of process templates are correct."""
    from gemd.entity.template.process_template import ProcessTemplate

    process_templates = [gem for gem in cake_gems if isinstance(gem, ProcessTemplate)]

    assert len(process_templates) == 4


def test_number_measurement_runs(cake_gems):
    """Tests that the number of measurement runs are correct."""
    measurement_runs = [gem for gem in cake_gems if isinstance(gem, MeasurementRun)]

    assert len(measurement_runs) == 8


def test_number_measurement_specs(cake_gems):
    """Tests that the number of measurement specs are correct."""
    measurement_specs = [gem for gem in cake_gems if isinstance(gem, MeasurementSpec)]

    assert len(measurement_specs) == 6


def test_number_measurement_templates(cake_gems):
    """Tests that the number of measurement templates are correct."""
    from gemd.entity.template.measurement_template import MeasurementTemplate

    measurement_templates = [gem for gem in cake_gems if isinstance(gem, MeasurementTemplate)]

    assert len(measurement_templates) == 4


def test_number_ingredient_runs(cake_gems):
    """Tests that the number of ingredient runs are correct."""
    ingredient_runs = [gem for gem in cake_gems if isinstance(gem, IngredientRun)]

    assert len(ingredient_runs) == 17


def test_number_ingredient_specs(cake_gems):
    """Tests that the number of ingredient specs are correct."""
    ingredient_specs = [gem for gem in cake_gems if isinstance(gem, IngredientSpec)]

    assert len(ingredient_specs) == 17


def test_number_property_templates(cake_gems):
    """Tests that the number of property templates are correct."""
    from gemd.entity.template.property_template import PropertyTemplate

    property_templates = [gem for gem in cake_gems if isinstance(gem, PropertyTemplate)]

    assert len(property_templates) == 6


def test_number_condition_templates(cake_gems):
    """Tests that the number of condition templates are correct."""
    from gemd.entity.template.condition_template import ConditionTemplate

    condition_templates = [gem for gem in cake_gems if isinstance(gem, ConditionTemplate)]

    assert len(condition_templates) == 3


def test_number_parameter_templates(cake_gems):
    """Tests that the number of parameter templates are correct."""
    from gemd.entity.template.parameter_template import ParameterTemplate

    parameter_templates = [gem for gem in cake_gems if isinstance(gem, ParameterTemplate)]

    assert len(parameter_templates) == 2
