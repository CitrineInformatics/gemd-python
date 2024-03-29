"""Test of the base attribute template."""
import pytest

from gemd.entity.bounds.categorical_bounds import CategoricalBounds
from gemd.entity.bounds.real_bounds import RealBounds
from gemd.entity.value.uniform_real import UniformReal
from gemd.entity.template.attribute_template import AttributeTemplate
from gemd.entity.template.property_template import PropertyTemplate
from gemd.entity.template.condition_template import ConditionTemplate
from gemd.entity.template.parameter_template import ParameterTemplate
from gemd.json import dumps, loads


class SampleAttributeTemplate(AttributeTemplate, typ="sample_attribute_template"):
    """A class to flex the base attribute template."""


cat_bounds = CategoricalBounds(categories={"a", "b", "c"})


def test_name_is_a_string():
    """Test that name is a string."""
    with pytest.raises(ValueError) as error:
        SampleAttributeTemplate(name=42, bounds=cat_bounds)

    assert "must be a string" in str(error.value)


def test_invalid_bounds():
    """Test that invalid bounds throw the appropriate error."""
    with pytest.raises(ValueError):
        SampleAttributeTemplate(name="name")  # Must have a bounds
    with pytest.raises(TypeError):
        SampleAttributeTemplate(name="name", bounds=UniformReal(0, 1, ''))


def test_json():
    """Test that json serialization round robins to the identity."""
    template = PropertyTemplate(name="foo", bounds=RealBounds(0, 1, ""))
    copy = loads(dumps(template))
    assert copy == template


def test_dependencies():
    """Test that dependency lists make sense."""
    targets = [
        PropertyTemplate(name="name", bounds=RealBounds(0, 1, '')),
        ConditionTemplate(name="name", bounds=RealBounds(0, 1, '')),
        ParameterTemplate(name="name", bounds=RealBounds(0, 1, '')),
    ]
    for target in targets:
        assert len(target.all_dependencies()) == 0, f"{type(target)} had dependencies"
