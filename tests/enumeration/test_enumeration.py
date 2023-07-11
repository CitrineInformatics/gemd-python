"""Tests of the enumeration class."""
import pytest
import warnings

from gemd.entity.attribute.property import Property
from gemd.enumeration import Origin
from gemd.enumeration.base_enumeration import BaseEnumeration, migrated_enum
from gemd.json import loads, dumps


def test_values():
    """Test that values can be validated and pulled from an enumeration."""
    class GoodClass(BaseEnumeration):
        RED = "Red"
        BLUE = "Blue"

    with pytest.deprecated_call():
        assert GoodClass.get_value("Red") == "Red"
    with pytest.deprecated_call():
        assert GoodClass.get_value(GoodClass.BLUE) == "Blue"
    with pytest.deprecated_call():
        assert GoodClass.get_value(None) is None
    with pytest.deprecated_call():
        assert GoodClass.get_enum("Red") == GoodClass.RED
    with pytest.deprecated_call():
        assert GoodClass.get_enum(GoodClass.BLUE) == GoodClass.BLUE
    with pytest.deprecated_call():
        assert GoodClass.get_enum(None) is None
    with pytest.deprecated_call():
        with pytest.raises(ValueError):
            GoodClass.get_value("Green")
    with pytest.deprecated_call():
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


def test_string_enum():
    """Test that the synonym mechanism works."""

    class TestEnum(BaseEnumeration):
        ONE = "One", "1"
        TWO = "Two", "2"

    assert TestEnum.ONE == "One", "Equality failed"
    assert str(TestEnum.ONE) == "One", "Equality failed, cast"
    assert TestEnum.ONE != "1", "Equality worked for synonym"
    assert TestEnum.from_str("One") == TestEnum.ONE, "from_str worked"
    assert TestEnum.from_str("ONE") == TestEnum.ONE, "from_str, caps worked"
    assert TestEnum.from_str("one") == TestEnum.ONE, "from_str, lower worked"
    assert TestEnum.from_str("1") == TestEnum.ONE, "from_str, synonym worked"
    assert TestEnum.from_str(None) is None, "from_str, bad returned None"
    assert TestEnum.from_str("1.0") is None, "from_str, bad returned None"
    with pytest.raises(ValueError, match="valid"):
        TestEnum.from_str("1.0", exception=True)
    for key in TestEnum.TWO.synonyms:
        assert key != TestEnum.TWO, f"Synonym {key} was equal?"
        assert TestEnum.from_str(key) == TestEnum.TWO, f"from_str didn't resolve {key}"
        assert (
                TestEnum.from_str(key.upper()) == TestEnum.TWO
        ), f"from_str didn't resolve {key.upper()}"


def test_missing():
    """Test that enumeration is resolved via multiple paths."""
    class TestEnum(BaseEnumeration):
        ONE = "One", "1"
        TWO = "Two", "2"

    assert TestEnum("One") == TestEnum.ONE
    assert TestEnum("ONE") == TestEnum.ONE
    assert TestEnum(TestEnum.ONE) == TestEnum.ONE
    assert TestEnum("1") == TestEnum.ONE

    with pytest.raises(ValueError):
        TestEnum("Uno")

    with pytest.raises(ValueError):
        TestEnum(1)


def test_migrated():
    """Verify that migration functions as expected."""
    @migrated_enum(old_value="UNO", new_value="ONE", deprecated_in="1.9.9", removed_in="2.0.0")
    class TestEnum(BaseEnumeration):
        ONE = "One", "1"
        TWO = "Two", "2"

    assert TestEnum.ONE == "One"

    with pytest.deprecated_call(match=r"ONE"):
        assert TestEnum.UNO == "One"

    with pytest.deprecated_call(match=r"ONE"):
        assert TestEnum["UNO"] == "One"

    with warnings.catch_warnings():
        warnings.simplefilter("error")
        assert TestEnum["ONE"] == "One"
