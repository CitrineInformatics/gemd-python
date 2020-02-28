"""Tests of the MaterialTemplate object."""
from taurus.entity.bounds.categorical_bounds import CategoricalBounds
from taurus.entity.template.property_template import PropertyTemplate
from taurus.entity.template.material_template import MaterialTemplate


property_template = PropertyTemplate(
    name="test_property", bounds=CategoricalBounds(["True", "False"])
)
material_template = MaterialTemplate(name="test_material", properties=[property_template])


def test_creating_material_spec():
    """Test creating a material spec from a material template."""

    material = material_template()  # inherit default properties from template
    assert material.name == material_template.name
    assert material.template is material_template
    for prop, (prop_template, bounds) in zip(material.properties, material_template.properties):
        assert prop.property.name == prop_template.name

    material = material_template(name='other name')  # change default values
    assert material.name == 'other name'
