"""Tests of property templates."""
from taurus.entity.attribute.property import Property
from taurus.entity.bounds.categorical_bounds import CategoricalBounds
from taurus.entity.bounds.real_bounds import RealBounds
from taurus.entity.template.property_template import PropertyTemplate
from taurus.entity.value.discrete_categorical import DiscreteCategorical
from taurus.entity.value.nominal_real import NominalReal
from taurus.entity.value.normal_real import NormalReal
from taurus.entity.value.uniform_real import UniformReal


def test_real_validation():
    """Test validation when the bounds is real."""
    desc = PropertyTemplate(
        name="test",
        bounds=RealBounds(lower_bound=-1, upper_bound=1.0, default_units='')
    )

    assert desc.validate(Property(name="test", value=NominalReal(0.5, ''))), \
        "Validate failed on a valid property"

    assert desc.validate(Property(name="test", value=NormalReal(0.95, 0.1, ''))), \
        "Validate failed on a valid property"

    assert desc.validate(
        Property(name="test", value=UniformReal(lower_bound=-0.7, upper_bound=0.2, units=''))
    ), "Validate failed on a valid property"

    assert not desc.validate(Property(name="foo", value=NominalReal(0.5, ''))), \
        "Validated passed on an invalid property"

    assert not desc.validate(Property(name="test", value=NominalReal(1.5, ''))), \
        "Validated passed on an invalid property"

    assert not desc.validate(Property(name="test", value=NormalReal(-1.5, 0.3, ''))), \
        "Validated passed on an invalid property"

    assert not desc.validate(Property(name="test", value=UniformReal(-0.9, 1.1, ''))), \
        "Validated passed on an invalid property"


def test_categorical_validation():
    """Test validation when the bounds are categorical."""
    desc = PropertyTemplate(
        name="test",
        bounds=CategoricalBounds(categories={"red", "black"})
    )

    assert desc.validate(Property(name="test", value=DiscreteCategorical("red"))), \
        "Validate failed on a valid property"
    assert desc.validate(
        Property(name="test", value=DiscreteCategorical({"red": 0.5, "black": 0.5}))
    ), "Validate failed on a valid property"

    assert not desc.validate(Property(name="foo", value=DiscreteCategorical("red"))), \
        "Validate passed on an invalid property"
    assert not desc.validate(Property(name="test", value=DiscreteCategorical("blue"))), \
        "Validate passed on an invalid property"
    assert not desc.validate(
        Property(name="test", value=DiscreteCategorical({"red": 1.0, "blue": 0.0}))
    ), "Validate passed on an invalid property"
