"""Test of the property template."""
from taurus.entity.template.property_template import PropertyTemplate
from taurus.entity.bounds.categorical_bounds import CategoricalBounds
from taurus.entity.value.nominal_categorical import NominalCategorical


property_template = PropertyTemplate(
    name="test_template", bounds=CategoricalBounds(["True", "False"])
)


def test_creating_property():
    """Test creating a property from a property template."""

    property = property_template()  # by default, inherit name and the template
    assert property.name == property_template.name
    assert property.template is property_template

    property = property_template(name='other name', value=NominalCategorical('True'))
    assert property.name != property_template.name
    assert property.name is not None
