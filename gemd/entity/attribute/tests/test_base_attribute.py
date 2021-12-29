"""Tests of the BaseAttribute class."""
import pytest

from gemd.entity.attribute.property import Property
from gemd.entity.template.process_template import ProcessTemplate
from gemd.entity.template.property_template import PropertyTemplate
from gemd.entity.value.nominal_real import NominalReal
from gemd.entity.bounds.real_bounds import RealBounds
from gemd.entity.bounds_validation import validation_context, WarningLevel


def test_invalid_assignment(caplog):
    """Test that invalid assignments throw the appropriate errors."""
    with pytest.raises(TypeError):
        Property(value=NominalReal(10, ''))
    with pytest.raises(TypeError):
        Property(name="property", value=10)
    with pytest.raises(TypeError):
        Property(name="property", template=ProcessTemplate("wrong kind of template"))
    with pytest.raises(ValueError):
        Property(name="property", origin=None)

    valid_prop = Property(name="property",
                          value=NominalReal(10, ''),
                          template=PropertyTemplate("template",
                                                    bounds=RealBounds(0, 100, '')
                                                    )
                          )
    good_val = valid_prop.value
    bad_val = NominalReal(-10.0, '')
    assert len(caplog.records) == 0, "Warning caught before logging tests were reached."
    with validation_context(WarningLevel.IGNORE):
        valid_prop.value = bad_val
        assert len(caplog.records) == 0, "Validation warned even though level is IGNORE."
        assert valid_prop.value == bad_val, "IGNORE allowed the bad value to be set."
        valid_prop.value = good_val
        assert len(caplog.records) == 0, "Validation warned even though level is IGNORE."
    with validation_context(WarningLevel.WARNING):
        valid_prop.value = bad_val
        assert len(caplog.records) == 1, "Validation didn't warn on out of bounds value."
        assert valid_prop.value == bad_val, "WARNING allowed the bad value to be set."
        valid_prop.value = good_val
        assert len(caplog.records) == 1, "Validation DID warn on a valid value."
    with validation_context(WarningLevel.FATAL):
        with pytest.raises(ValueError):
            valid_prop.value = bad_val
        assert valid_prop.value == good_val, "FATAL didn't allow the bad value to be set."

    with validation_context(WarningLevel.FATAL):
        with pytest.raises(ValueError):
            valid_prop.template = PropertyTemplate("template",
                                                   bounds=RealBounds(0, 1, '')
                                                   )
        assert valid_prop.value == good_val, "FATAL didn't allow the bad value to be set."
