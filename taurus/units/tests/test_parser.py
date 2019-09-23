import pytest
from taurus.units import parse_units, UndefinedUnitError


def test_parse_expected():
    """Test that we can parse the units that we expect to be able to."""
    expected = [
        "degC", "degF", "K",
        "g", "kg", "mg", "ton",
        "L", "mL",
        "inch", "ft", "mm", "um",
        "second", "ms", "hour", "minute", "ns",
        "g/cm^3", "g/mL", "kg/cm^3"
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
        "St"
    ]
    for unit in unexpected:
        with pytest.raises(UndefinedUnitError):
            parse_units(unit)


def test_delta_units():
    parse_units('delta_degF / hr')
