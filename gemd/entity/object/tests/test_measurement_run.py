"""Tests of the measurement run object."""
import pytest
from uuid import uuid4

from gemd.json import dumps, loads
from gemd.entity.bounds import IntegerBounds
from gemd.entity.object import MeasurementRun, MaterialRun
from gemd.entity.object.measurement_spec import MeasurementSpec
from gemd.entity.attribute import Condition, Parameter, Property
from gemd.entity.template import ConditionTemplate, ParameterTemplate, PropertyTemplate
from gemd.entity.source.performed_source import PerformedSource
from gemd.entity.template import MeasurementTemplate, PropertyTemplate, ParameterTemplate, \
    ConditionTemplate
from gemd.entity.value import NominalReal, NominalInteger
from gemd.entity.file_link import FileLink
from gemd.entity.link_by_uid import LinkByUID
from gemd.entity.bounds import RealBounds
from gemd.entity.bounds_validation import validation_context, WarningLevel
from gemd.util.impl import substitute_links


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
    measurement = MeasurementRun("The Measurement", conditions=condition, spec=spec)

    copy = loads(dumps(measurement))
    assert dumps(copy.spec) == dumps(measurement.spec), \
        "Measurement spec should be preserved if measurement run is serialized"


def test_material_soft_link():
    """Test that a measurement run can link to a material run, and that it survives serde."""
    dye = MaterialRun("rhodamine", file_links=FileLink(filename='a.csv', url='/a/path'))
    assert dye.measurements == [], "default value of .measurements should be an empty list"

    # The .measurements member should not be settable
    with pytest.raises(AttributeError):
        dye.measurements = [MeasurementRun("Dummy")]

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

    assert 'measurements' in repr(dye)
    assert 'material' in repr(fluorescence)
    assert 'material' in repr(absorbance)

    subbed = substitute_links(dye)
    assert 'measurements' in repr(subbed)


def test_material_id_link():
    """Check that a measurement can be linked to a material that is a LinkByUID."""
    mat = LinkByUID('id', str(uuid4()))
    meas = MeasurementRun("name", material=mat)
    assert meas.material == mat
    assert loads(dumps(meas)) == meas


def test_source():
    """Test that source can be set, serialized, and deserialized."""
    source = PerformedSource(performed_by="Marie Curie", performed_date="1898-07-01")
    measurement = MeasurementRun(name="Polonium", source=source)
    assert loads(dumps(measurement)).source.performed_by == "Marie Curie"

    with pytest.raises(TypeError):
        MeasurementRun(name="Polonium", source="Marie Curie on 1898-07-01")


def test_measurement_reassignment():
    """Check that a measurement run can be re-assigned to a new material run."""
    sample1 = MaterialRun("Sample 1")
    sample2 = MaterialRun("Sample 2")
    mass = MeasurementRun("Mass of sample", material=sample1)
    volume = MeasurementRun("Volume of sample", material=sample1)
    assert mass.material == sample1
    assert set(sample1.measurements) == {mass, volume}
    assert sample2.measurements == []

    mass.material = sample2
    assert mass.material == sample2
    assert sample1.measurements == [volume]
    assert sample2.measurements == [mass]

    mass.material = None
    assert mass.material is None
    assert sample2.measurements == []


def test_invalid_assignment():
    """Invalid assignments to `material` or `spec` throw a TypeError."""
    with pytest.raises(TypeError):
        MeasurementRun("name", spec=Condition("value of pi", value=NominalReal(3.14159, '')))
    with pytest.raises(TypeError):
        MeasurementRun("name", material=FileLink("filename", "url"))
    with pytest.raises(TypeError):
        MeasurementRun()  # Name is required


def test_template_validations(caplog):
    """Make sure template validations and level controls behave as expected."""
    msr_tmpl = MeasurementTemplate(
        name="Measurement Template",
        properties=[PropertyTemplate("Name", bounds=RealBounds(0, 1, ""))],
        conditions=[ConditionTemplate("Name", bounds=RealBounds(0, 1, ""))],
        parameters=[ParameterTemplate("Name", bounds=RealBounds(0, 1, ""))],
    )
    msr_spec = MeasurementSpec("Measurement Spec", template=msr_tmpl)
    msr_run = MeasurementRun("MeasurementRun", spec=msr_spec)
    with validation_context(WarningLevel.IGNORE):
        msr_run.properties.append(Property("Name", value=NominalReal(-1, "")))
        msr_run.conditions.append(Condition("Name", value=NominalReal(-1, "")))
        msr_run.parameters.append(Parameter("Name", value=NominalReal(-1, "")))
        assert len(caplog.records) == 0, "Logging records wasn't empty"
    with validation_context(WarningLevel.WARNING):
        msr_run.properties.append(Property("Name", value=NominalReal(-1, "")))
        assert len(caplog.records) == 1, "WARNING didn't warn on invalid Property."
        msr_run.conditions.append(Condition("Name", value=NominalReal(-1, "")))
        assert len(caplog.records) == 2, "WARNING didn't warn on invalid Condition."
        msr_run.parameters.append(Parameter("Name", value=NominalReal(-1, "")))
        assert len(caplog.records) == 3, "WARNING didn't warn on invalid Parameter."
    with validation_context(WarningLevel.FATAL):
        with pytest.raises(ValueError):
            msr_run.properties.append(Property("Name", value=NominalReal(-1, "")))
        with pytest.raises(ValueError):
            msr_run.conditions.append(Condition("Name", value=NominalReal(-1, "")))
        with pytest.raises(ValueError):
            msr_run.parameters.append(Parameter("Name", value=NominalReal(-1, "")))


def test_template_access():
    """A measurement run's template should be equal to its spec's template."""
    template = MeasurementTemplate("measurement template", uids={'id': str(uuid4())})
    spec = MeasurementSpec("A spec", uids={'id': str(uuid4())}, template=template)
    meas = MeasurementRun("A run", uids={'id': str(uuid4())}, spec=spec)
    assert meas.template == template

    meas.spec = LinkByUID.from_entity(spec)
    assert meas.template is None


def test_dependencies():
    """Test that dependency lists make sense."""
    prop = PropertyTemplate(name="name", bounds=IntegerBounds(0, 1))
    cond = ConditionTemplate(name="name", bounds=IntegerBounds(0, 1))
    param = ParameterTemplate(name="name", bounds=IntegerBounds(0, 1))

    template = MeasurementTemplate("measurement template",
                                   parameters=[param],
                                   conditions=[cond],
                                   properties=[prop])
    spec = MeasurementSpec("A spec", template=template)
    mat = MaterialRun(name="mr")
    meas = MeasurementRun("A run", spec=spec, material=mat,
                          properties=[
                              Property(prop.name, template=prop, value=NominalInteger(1))
                          ],
                          conditions=[
                              Condition(cond.name, template=cond, value=NominalInteger(1))
                          ],
                          parameters=[
                              Parameter(param.name, template=param, value=NominalInteger(1))
                          ]
                          )

    assert template not in meas.all_dependencies()
    assert spec in meas.all_dependencies()
    assert mat in meas.all_dependencies()
    assert prop in meas.all_dependencies()
    assert cond in meas.all_dependencies()
    assert param in meas.all_dependencies()
