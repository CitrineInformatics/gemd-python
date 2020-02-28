"""Tests of the MeasurementTemplate object."""
from taurus.entity.bounds.categorical_bounds import CategoricalBounds
from taurus.entity.template.parameter_template import ParameterTemplate
from taurus.entity.template.condition_template import ConditionTemplate
from taurus.entity.template.measurement_template import MeasurementTemplate


condition_template = ConditionTemplate(
    name="test_condition", bounds=CategoricalBounds(["True", "False"])
)
parameter_template = ParameterTemplate(
    name="test_parameter", bounds=CategoricalBounds(["True", "False"])
)
measurement_template = MeasurementTemplate(
    name="test_measurement", conditions=[condition_template], parameters=[parameter_template]
)


def test_creating_measurement_spec():
    """Test creating a measurement spec from a measurement template."""

    measurement = measurement_template()  # inherit default properties from template
    assert measurement.name == measurement_template.name
    assert measurement.template is measurement_template

    for cond, (cond_template, bounds) in zip(
        measurement.conditions, measurement_template.conditions
    ):
        assert cond.name == cond_template.name

    for param, (param_template, bounds) in zip(
        measurement.parameters, measurement_template.parameters
    ):
        assert param.name == param_template.name

    measurement = measurement_template(name="other name")  # change default values
    assert measurement.name == "other name"
