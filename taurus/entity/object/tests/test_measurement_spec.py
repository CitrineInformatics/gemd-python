"""Tests of the MaterialTemplate object."""
from taurus.entity.object.measurement_spec import MeasurementSpec
from taurus.entity.attribute.parameter import Parameter
from taurus.entity.value.nominal_real import NominalReal


measurement_spec = MeasurementSpec(
    name="test measurement",
    parameters=[Parameter(name="test parameter", value=NominalReal(1.0, "N"))],
)


def test_creating_measurement_run():
    """Test creating a measurement run from a measurement spec."""

    measurement = measurement_spec()  # inherit default attributes from spec
    assert measurement.name == measurement_spec.name
    assert measurement.spec is measurement_spec
    for spec_pram, run_param in zip(measurement.parameters, measurement_spec.parameters):
        assert spec_pram == run_param
        assert spec_pram is not run_param

    measurement = measurement_spec(name="other name")  # change default values
    assert measurement.name == "other name"
