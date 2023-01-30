import pytest
import pkg_resources
from contextlib import contextmanager
from pint import UnitRegistry
from gemd.units import parse_units, convert_units, change_definitions_file, UndefinedUnitError


def test_parse_expected():
    """Test that we can parse the units that we expect to be able to."""
    # use the default unit registry for now
    reg = UnitRegistry(filename=pkg_resources.resource_filename("gemd.units", "citrine_en.txt"))

    expected = [
        "degC", "degF", "K",
        "g", "kg", "mg", "ton",
        "L", "mL",
        "inch", "ft", "mm", "um",
        "second", "ms", "hour", "minute", "ns",
        "g/cm^3", "g/mL", "kg/cm^3",
        reg("kg").u,
        "amu",  # A line that was edited
        "Seconds",  # Added support for some title-case units
        "delta_Celsius / hour",  # Added to make sure pint version is right (>0.10)
        "g / 2.5 cm",  # Scaling factors are acceptable
    ]
    for unit in expected:
        parse_units(unit)
    assert parse_units("") == 'dimensionless'
    # Scaling factors bind tightly to trailing units
    assert parse_units("g / 2.5 cm") == parse_units("g / (2.5 cm)")
    assert parse_units("g / 2.5 * cm") == parse_units("g cm / 2.5")


def test_parse_unexpected():
    """Test that we cannot parse the units that we do not expect to."""
    unexpected = [
        "gibberish",
        5,
        "cp",  # Removed because of risk of collision with cP
        "chain",  # Survey units eliminated
        "SECONDS"  # Not just case insensitivity
    ]
    for unit in unexpected:
        with pytest.raises(UndefinedUnitError):
            parse_units(unit)


def test_parse_none():
    """Test that None parses as None."""
    assert parse_units(None) is None


def test_conversion():
    """Tests that check if particular units are interoperable."""
    conversions = {"in_lb": "foot_pound"}
    for source, dest in conversions.items():
        assert convert_units(convert_units(1, source, dest), dest, source) == 1


@contextmanager
def _change_units(filename):
    try:
        change_definitions_file(filename)
        yield
    finally:
        change_definitions_file()


def test_file_change():
    """Test that swapping units files works."""
    assert convert_units(1, 'm', 'cm') == 100
    with pytest.raises(UndefinedUnitError):
        assert convert_units(1, 'usd', 'USD') == 1
    with _change_units(filename=pkg_resources.resource_filename("gemd.units",
                                                                "tests/test_units.txt")):
        with pytest.raises(UndefinedUnitError):
            assert convert_units(1, 'm', 'cm') == 100
        assert convert_units(1, 'usd', 'USD') == 1
    assert convert_units(1, 'm', 'cm') == 100  # And verify we're back to normal
