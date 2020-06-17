"""Tests of the BaseAttribute class."""
import pytest

from gemd.entity.attribute.property import Property
from gemd.entity.template.process_template import ProcessTemplate
from gemd.entity.value.nominal_real import NominalReal


def test_invalid_assignment():
    """Test that invalid assignments throw the appropriate errors."""
    with pytest.raises(TypeError):
        Property(value=NominalReal(10, ''))
    with pytest.raises(TypeError):
        Property(name="property", value=10)
    with pytest.raises(TypeError):
        Property(name="property", template=ProcessTemplate("wrong kind of template"))
    with pytest.raises(ValueError):
        Property(name="property", origin=None)
