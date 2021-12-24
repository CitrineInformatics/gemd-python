import pytest

from gemd.entity.attribute.property_and_conditions import Property, Condition, \
    PropertyAndConditions
from gemd.entity.link_by_uid import LinkByUID
from gemd.entity.template.property_template import PropertyTemplate
from gemd.entity.template.condition_template import ConditionTemplate
from gemd.entity.value.nominal_integer import NominalInteger
from gemd.entity.value.nominal_categorical import NominalCategorical
from gemd.entity.bounds.integer_bounds import IntegerBounds
from gemd.entity.bounds.categorical_bounds import CategoricalBounds


def test_fields_from_property():
    """Test that several fields of the attribute are derived from the property."""
    prop_template = PropertyTemplate(name="cookie eating template", bounds=IntegerBounds(0, 1000))
    cond_template = ConditionTemplate(name="Hunger template",
                                      bounds=CategoricalBounds(["hungry", "full", "peckish"]))
    prop = Property(name="number of cookies eaten",
                    template=prop_template,
                    origin='measured',
                    value=NominalInteger(27))
    cond = Condition(name="hunger level",
                     template=cond_template,
                     origin='specified',
                     value=NominalCategorical("hungry"))

    prop_and_conds = PropertyAndConditions(property=prop, conditions=[cond])
    assert prop_and_conds.name == prop.name
    assert prop_and_conds.template == prop.template
    assert prop_and_conds.origin == prop.origin
    assert prop_and_conds.value == prop.value


def test_invalid_assignment():
    """Test that invalid assignment throws a TypeError."""
    with pytest.raises(TypeError):
        PropertyAndConditions(property=LinkByUID('id', 'a15'))
    with pytest.raises(TypeError):
        PropertyAndConditions(property=Property("property"),
                              conditions=[Condition("condition"), LinkByUID('scope', 'id')])


def test_unsupported_template():
    """Test that direct assignment of a template raises a useful error."""
    prop_template = PropertyTemplate(name="cookie eating template", bounds=IntegerBounds(0, 1000))
    prop = Property(name="number of cookies eaten",
                    template=prop_template,
                    origin='measured',
                    value=NominalInteger(27))
    with pytest.raises(AttributeError):
        PropertyAndConditions(property=prop).template = None
    with pytest.raises(AttributeError):
        PropertyAndConditions(property=prop).template = prop_template
