"""Test of the parameter template."""
from taurus.entity.template.parameter_template import ParameterTemplate
from taurus.entity.bounds.categorical_bounds import CategoricalBounds
from taurus.entity.value.nominal_categorical import NominalCategorical


parameter_template = ParameterTemplate(
    name="test_template", bounds=CategoricalBounds(["True", "False"])
)


def test_creating_parameter():
    """Test creating a parameter from a parameter template."""

    parameter = parameter_template()  # by default, inherit name and the template
    assert parameter.name == parameter_template.name
    assert parameter.template is parameter_template

    parameter = parameter_template(name='other name', value=NominalCategorical('True'))
    assert parameter.name != parameter_template.name
    assert parameter.name is not None
