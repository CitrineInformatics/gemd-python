"""Tests of the measurement run object."""
import pytest
from uuid import uuid4

from taurus.client.json_encoder import dumps, loads
from taurus.entity.object import MeasurementRun, MaterialRun
from taurus.entity.object.measurement_spec import MeasurementSpec
from taurus.entity.attribute.condition import Condition
from taurus.entity.attribute.parameter import Parameter
from taurus.entity.attribute.property import Property
from taurus.entity.source.performed_source import PerformedSource
from taurus.entity.value.nominal_real import NominalReal
from taurus.entity.file_link import FileLink
from taurus.entity.link_by_uid import LinkByUID


def test_measurement_spec():
    """Test the measurement spec/run connection survives ser/de."""
    condition = Condition(name="Temp condition", value=NominalReal(nominal=298, units='kelvin'))
    parameter = Parameter(name="Important parameter")
    spec = MeasurementSpec(
        name="Precise way to do a measurement",
        parameters=parameter,
        conditions=condition
    )

    # Create a measurement run from this measurement spec
    measurement = MeasurementRun(conditions=condition, spec=spec)

    copy = loads(dumps(measurement))
    assert dumps(copy.spec) == dumps(measurement.spec), \
        "Measurement spec should be preserved if measurement run is serialized"


def test_material_soft_link():
    """Test that a measurement run can link to a material run, and that it survives serde."""
    dye = MaterialRun("rhodamine", file_links=FileLink(filename='a.csv', url='/a/path'))
    assert dye.measurements == [], "default value of .measurements should be an empty list"

    # The .measurements member should not be settable
    with pytest.raises(AttributeError):
        dye.measurements = [MeasurementRun()]

    absorbance = MeasurementRun(
        name="Absorbance",
        uids={'id': str(uuid4())},
        properties=[Property(name='Abs at 500 nm', value=NominalReal(0.1, ''))]
    )
    assert absorbance.material is None, "Measurements should have None as the material by default"
    absorbance.material = dye
    assert absorbance.material == dye, "Material not set correctly for measurement"
    assert dye.measurements == [absorbance], "Soft-link from material to measurement not created"

    fluorescence = MeasurementRun(
        name="Fluorescence",
        uids={'id': str(uuid4())},
        properties=[Property(name='PL counts at 550 nm', value=NominalReal(30000, ''))],
        material=dye
    )

    assert fluorescence.material == dye, "Material not set correctly for measurement"
    assert dye.measurements == [absorbance, fluorescence], \
        "Soft-link from material to measurements not created"

    assert loads(dumps(absorbance)) == absorbance, \
        "Measurement should remain unchanged when serialized"
    assert loads(dumps(fluorescence)) == fluorescence, \
        "Measurement should remain unchanged when serialized"

    # Serializing the material breaks the material-->measurement link.
    assert loads(dumps(dye)).measurements == [], \
        "Measurement information should be removed when material is serialized"

    assert 'measurements' in dye.__repr__()
    assert 'material' in fluorescence.__repr__()
    assert 'material' in absorbance.__repr__()


def test_material_id_link():
    """Check that a measurement can be linked to a material that is a LinkByUID."""
    mat = LinkByUID('id', str(uuid4()))
    meas = MeasurementRun(material=mat)
    assert meas.material == mat
    assert loads(dumps(meas)) == meas


def test_source():
    """Test that source can be set, serialized, and deserialized."""
    source = PerformedSource(performed_by="Marie Curie", performed_date="1898-07-01")
    measurement = MeasurementRun(name="Polonium", source=source)
    assert loads(dumps(measurement)).source.performed_by == "Marie Curie"

    with pytest.raises(TypeError):
        MeasurementRun(name="Polonium", source="Marie Curie on 1898-07-01")
