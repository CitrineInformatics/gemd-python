import pytest
import pkg_resources
from pint import UnitRegistry
from taurus.units import parse_units, UndefinedUnitError

# use the default unit registry for now
_ureg = UnitRegistry(filename=pkg_resources.resource_filename("taurus.units", "citrine_en.txt"))


def test_parse_expected():
    """Test that we can parse the units that we expect to be able to."""
    expected = [
        "degC", "degF", "K",
        "g", "kg", "mg", "ton",
        "L", "mL",
        "inch", "ft", "mm", "um",
        "second", "ms", "hour", "minute", "ns",
        "g/cm^3", "g/mL", "kg/cm^3",
        _ureg("kg").u
    ]
    for unit in expected:
        parse_units(unit)


def test_parse_unexpected():
    """Test that we cannot parse the units that we do not expect to."""
    unexpected = [
        "rankine",
        "slug",
        "hand",
        "year",
        "St",
        5
    ]
    for unit in unexpected:
        with pytest.raises(UndefinedUnitError):
            parse_units(unit)


def test_parse_none():
    """Test that None parses as None."""
    assert parse_units(None) is None
