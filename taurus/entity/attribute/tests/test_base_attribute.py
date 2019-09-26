"""Tests of the BaseAttribute class."""
import pytest

from taurus.entity.attribute.property import Property
from taurus.entity.template.process_template import ProcessTemplate
from taurus.entity.value.nominal_real import NominalReal


def test_invalid_assignment():
    """Test that invalid assignments throw the appropriate errors."""
    with pytest.raises(ValueError):
        Property(value=NominalReal(10, ''))
    with pytest.raises(TypeError):
        Property(name="property", value=10)
    with pytest.raises(TypeError):
        Property(name="property", template=ProcessTemplate("wrong kind of template"))
    with pytest.raises(ValueError):
        Property(name="property", origin=None)
