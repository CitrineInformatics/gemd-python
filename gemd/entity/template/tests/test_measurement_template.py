import pytest

from gemd.entity.bounds import IntegerBounds
from gemd.entity.value import NominalInteger
from gemd.entity.attribute import Condition, Property, Parameter, PropertyAndConditions
from gemd.entity.template import MeasurementTemplate, PropertyTemplate, ConditionTemplate, \
    ParameterTemplate
from gemd.entity.template.attribute_template import AttributeTemplate
from gemd.entity.bounds.base_bounds import BaseBounds
from gemd.entity.valid_list import ValidList


def test_mixins():
    """Measurement templates have all 3 mixin traits."""
    obj = MeasurementTemplate("Name",
                              properties=[PropertyTemplate("Name", bounds=IntegerBounds(0, 1))],
                              conditions=[ConditionTemplate("Name", bounds=IntegerBounds(0, 1))],
                              parameters=[ParameterTemplate("Name", bounds=IntegerBounds(0, 1))],
                              )
    with pytest.raises(TypeError):
        obj.properties.append(ConditionTemplate("3", bounds=IntegerBounds(0, 5)))
    with pytest.raises(TypeError):
        obj.properties.append(ParameterTemplate("3", bounds=IntegerBounds(0, 5)))

    with pytest.raises(TypeError):
        obj.conditions.append(PropertyTemplate("3", bounds=IntegerBounds(0, 5)))
    with pytest.raises(TypeError):
        obj.conditions.append(ParameterTemplate("3", bounds=IntegerBounds(0, 5)))

    with pytest.raises(TypeError):
        obj.parameters.append(ConditionTemplate("3", bounds=IntegerBounds(0, 5)))
    with pytest.raises(TypeError):
        obj.parameters.append(PropertyTemplate("3", bounds=IntegerBounds(0, 5)))

    with pytest.raises(TypeError):  # You passed a `scalar` to extend
        obj.properties.extend((PropertyTemplate("3", bounds=IntegerBounds(0, 5)),
                               IntegerBounds(1, 3)))

    with pytest.raises(ValueError):  # You passed a `scalar` to extend
        obj.properties = (PropertyTemplate("3", bounds=IntegerBounds(1, 3)),
                          IntegerBounds(0, 5))

    obj.properties.append((PropertyTemplate("2", bounds=IntegerBounds(0, 5)),
                           IntegerBounds(1, 3)))
    obj.properties.extend([PropertyTemplate("3", bounds=IntegerBounds(0, 5)),
                           (PropertyTemplate("4", bounds=IntegerBounds(0, 5)),
                            IntegerBounds(1, 3))
                           ])
    obj.conditions.insert(1, ConditionTemplate("2", bounds=IntegerBounds(0, 1)))
    obj.parameters[0] = ParameterTemplate("Name", bounds=IntegerBounds(0, 1))

    for x in (obj.properties, obj.conditions, obj.parameters):
        assert isinstance(x, ValidList)
        for y in x:
            assert isinstance(y, list)
            assert len(y) == 2
            assert isinstance(y[0], AttributeTemplate)
            if y[1] is not None:
                assert isinstance(y[1], BaseBounds)

    second = MeasurementTemplate("Name",
                                 properties=[PropertyTemplate("Name", bounds=IntegerBounds(0, 1)),
                                             IntegerBounds(0, 1)
                                             ],
                                 conditions=[ConditionTemplate("Name", bounds=IntegerBounds(0, 1)),
                                             IntegerBounds(0, 1)
                                             ],
                                 parameters=[ParameterTemplate("Name", bounds=IntegerBounds(0, 1)),
                                             IntegerBounds(0, 1)
                                             ],
                                 )
    assert len(second.properties) == 1
    assert len(second.conditions) == 1
    assert len(second.parameters) == 1

    good_val = NominalInteger(1)
    bad_val = NominalInteger(2)

    assert second.validate_condition(Condition("Other name",
                                               value=good_val,
                                               template=second.conditions[0][0])), \
        "Condition with template and good value didn't validate."
    assert not second.validate_condition(Condition("Other name",
                                                   value=bad_val,
                                                   template=second.conditions[0][0])), \
        "Condition with template and bad value DID validate."
    assert second.validate_parameter(Parameter("Other name",
                                               value=good_val,
                                               template=second.parameters[0][0])), \
        "Parameter with template and good value didn't validate."
    assert not second.validate_parameter(Parameter("Other name",
                                                   value=bad_val,
                                                   template=second.parameters[0][0])), \
        "Parameter with template and bad value DID validate."
    assert second.validate_property(Property("Other name",
                                             value=good_val,
                                             template=second.properties[0][0])), \
        "Property with template and good value didn't validate."
    assert not second.validate_property(Property("Other name",
                                                 value=bad_val,
                                                 template=second.properties[0][0])), \
        "Property with template and bad value DID validate."

    assert second.validate_condition(Condition("Name", value=good_val)), \
        "Condition without template and good value didn't validate."
    assert not second.validate_condition(Condition("Name", value=bad_val)), \
        "Condition without template and bad value DID validate."
    assert second.validate_parameter(Parameter("Name", value=good_val)), \
        "Parameter without template and good value didn't validate."
    assert not second.validate_parameter(Parameter("Name", value=bad_val)), \
        "Parameter without template and bad value DID validate."
    assert second.validate_property(Property("Name", value=good_val)), \
        "Property without template and good value didn't validate."
    assert not second.validate_property(Property("Name", value=bad_val)), \
        "Property without template and bad value DID validate."

    assert second.validate_condition(Condition("Other name", value=bad_val)), \
        "Unmatched condition and bad value didn't validate."
    assert second.validate_parameter(Parameter("Other name", value=bad_val)), \
        "Unmatched parameter and bad value didn't validate."
    assert second.validate_property(Property("Other name", value=bad_val)), \
        "Unmatched property and bad value didn't validate."

    second.conditions[0][1] = None
    second.parameters[0][1] = None
    second.properties[0][1] = None
    assert second.validate_condition(Condition("Name", value=good_val)), \
        "Condition and good value with passthrough didn't validate."
    assert second.validate_parameter(Parameter("Name", value=good_val)), \
        "Parameter and good value with passthrough didn't validate."
    assert second.validate_property(Property("Name", value=good_val)), \
        "Property and good value with passthrough didn't validate."
    assert second.validate_property(
        PropertyAndConditions(property=Property("Name", value=good_val))), \
        "PropertyAndConditions didn't fall back to Property."


def test_dependencies():
    """Test that dependency lists make sense."""
    prop = PropertyTemplate(name="name", bounds=IntegerBounds(0, 1))
    cond = ConditionTemplate(name="name", bounds=IntegerBounds(0, 1))
    param = ParameterTemplate(name="name", bounds=IntegerBounds(0, 1))

    msr_template = MeasurementTemplate("a process template",
                                       conditions=[cond],
                                       properties=[prop],
                                       parameters=[param])
    assert prop in msr_template.all_dependencies()
    assert cond in msr_template.all_dependencies()
    assert param in msr_template.all_dependencies()


def test_links_as_templates():
    """Verify that LinkByUIDs don't break anything we could have otherwise done."""
    prop_tmpl = PropertyTemplate("Name", uids={"scope": "prop"}, bounds=IntegerBounds(1, 5))
    cond_tmpl = ConditionTemplate("Name", uids={"scope": "cond"}, bounds=IntegerBounds(1, 5))
    param_tmpl = ParameterTemplate("Name", uids={"scope": "param"}, bounds=IntegerBounds(1, 5))
    no_bounds = MeasurementTemplate("Name",
                                    properties=[prop_tmpl],
                                    conditions=[cond_tmpl],
                                    parameters=[param_tmpl],
                                    )

    just_right = NominalInteger(2)
    middling = NominalInteger(4)
    too_high = NominalInteger(7)

    scenarios = [
        ("property", Property, MeasurementTemplate.validate_property, prop_tmpl),
        ("condition", Condition, MeasurementTemplate.validate_condition, cond_tmpl),
        ("parameter", Parameter, MeasurementTemplate.validate_parameter, param_tmpl),
    ]

    # Check that Attributes are checked against the template when the attributes links
    for scenario in scenarios:
        name, attr, validate, tmpl = scenario

        assert validate(no_bounds,
                        attr("Other name", template=tmpl.to_link(), value=middling)), \
            f"{name} didn't validate with {name}.template as LinkByUID."
        assert not validate(no_bounds,
                            attr("Other name", template=tmpl.to_link(), value=too_high)), \
            f"{name} DID validate with {name}.template as LinkByUID and bad value."

    with_bounds = MeasurementTemplate("Name",
                                      properties=[(prop_tmpl.to_link(), IntegerBounds(1, 3))],
                                      conditions=[(cond_tmpl.to_link(), IntegerBounds(1, 3))],
                                      parameters=[(param_tmpl.to_link(), IntegerBounds(1, 3))],
                                      )

    # Check that Attributes are checked against the bounds when the attributes links
    for scenario in scenarios:
        name, attr, validate, tmpl = scenario

        assert validate(with_bounds,
                        attr("Other name", template=tmpl.to_link(), value=just_right)), \
            f"{name} didn't validate with {name}.template as LinkByUID and bounds."
        assert not validate(with_bounds,
                            attr("Other name", template=tmpl.to_link(), value=middling)), \
            f"{name} DID validate with {name}.template as LinkByUID, bad value, and bounds."

    with_links = MeasurementTemplate("Name",
                                     properties=[(prop_tmpl.to_link())],
                                     conditions=[(cond_tmpl.to_link())],
                                     parameters=[(param_tmpl.to_link())],
                                     )

    # Check that tests pass when there's no way to test
    for scenario in scenarios:
        name, attr, validate, tmpl = scenario

        assert validate(with_links,
                        attr("Other name", template=tmpl.to_link(), value=too_high)), \
            f"{name} didn't validate with LinkByUID for everything."
