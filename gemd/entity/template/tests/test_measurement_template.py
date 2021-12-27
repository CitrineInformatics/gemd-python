import pytest

from gemd.entity.bounds import IntegerBounds
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
