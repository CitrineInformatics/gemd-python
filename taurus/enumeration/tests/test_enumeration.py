"""Tests of the enumeration class."""
import pytest

from taurus.entity.attribute.property import Property
from taurus.enumeration import Origin
from taurus.enumeration.base_enumeration import BaseEnumeration
from taurus.client.json_encoder import loads, dumps


def test_values():
    """Test that values can be validated and pulled from an enumeration."""
    class GoodClass(BaseEnumeration):
        RED = "Red"
        BLUE = "Blue"

    assert GoodClass.get_value("Red") == "Red"
    assert GoodClass.get_value(GoodClass.BLUE) == "Blue"
    assert GoodClass.get_value(None) is None
    assert GoodClass.get_enum("Red") == GoodClass.RED
    assert GoodClass.get_enum(GoodClass.BLUE) == GoodClass.BLUE
    assert GoodClass.get_enum(None) is None
    with pytest.raises(ValueError):
        GoodClass.get_value("Green")
    with pytest.raises(ValueError):
        GoodClass.get_enum("Green")


def test_json_serde():
    """Test that values can be ser/de using our custom json loads/dumps."""
    # Enums are only used in the context of another class --
    # it is not possible to deserialize to enum with the current
    # serialization strategy (plain string) without this context.
    original = Property(name="foo", origin=Origin.MEASURED)
    copy = loads(dumps(original))
    assert original == copy


def test_restrictions():
    """Test that restrictions apply to enumerations--all values must be unique strings."""
    with pytest.raises(ValueError):
        class BadClass1(BaseEnumeration):
            RED = "red"
            BLUE = "blue"
            MAROON = "red"

    with pytest.raises(ValueError):
        class BadClass2(BaseEnumeration):
            FIRST = "one"
            SECOND = 2
