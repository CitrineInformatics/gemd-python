"""Test of the condition template."""
from taurus.entity.template.condition_template import ConditionTemplate
from taurus.entity.bounds.categorical_bounds import CategoricalBounds
from taurus.entity.value.nominal_categorical import NominalCategorical


condition_template = ConditionTemplate(
    name="test_template", bounds=CategoricalBounds(["True", "False"])
)


def test_creating_condition():
    """Test creating a condition from a condition template."""

    condition = condition_template()  # by default, inherit name and the template
    assert condition.name == condition_template.name
    assert condition.template is condition_template

    condition = condition_template(name='other name', value=NominalCategorical('True'))
    assert condition.name != condition_template.name
    assert condition.name is not None
