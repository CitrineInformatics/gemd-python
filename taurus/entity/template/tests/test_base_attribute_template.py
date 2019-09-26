"""Test of the base attribute template."""
import pytest

from taurus.entity.bounds.categorical_bounds import CategoricalBounds
from taurus.entity.bounds.real_bounds import RealBounds
from taurus.entity.template.attribute_template import AttributeTemplate
from taurus.entity.template.property_template import PropertyTemplate
from taurus.client.json_encoder import dumps, loads


class SampleAttributeTemplate(AttributeTemplate):
    """A class to flex the base attribute template."""

    typ = "sample_attribute_template"


cat_bounds = CategoricalBounds(categories={"a", "b", "c"})


def test_name_is_a_string():
    """Test that name is a string."""
    with pytest.raises(ValueError) as error:
        SampleAttributeTemplate(name=42, bounds=cat_bounds)

    assert "must be a string" in str(error.value)


def test_json():
    """Test that json serialization round robins to the identity."""
    template = PropertyTemplate(name="foo", bounds=RealBounds(0, 1, ""))
    copy = loads(dumps(template))
    assert copy == template
