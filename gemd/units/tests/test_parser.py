import re

import pytest
import pkg_resources
from contextlib import contextmanager
from pint import UnitRegistry
from gemd.units import parse_units, convert_units, change_definitions_file, \
    UndefinedUnitError, DefinitionSyntaxError


def test_parse_expected():
    """Test that we can parse the units that we expect to be able to."""
    # use the default unit registry for now
    reg = UnitRegistry(filename=pkg_resources.resource_filename("gemd.units", "citrine_en.txt"))

    # Pint's parse_units actually gets this wrong
    assert parse_units("m^-1 * newton / meter") == parse_units("N / m^2")

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
        "g / -+-25e-1 m"  # Weird but fine
    ]
    for unit in expected:
        parse_units(unit)
    assert parse_units("") == 'dimensionless'
    # Scaling factors bind tightly to trailing units
    assert parse_units("g / 2.5 cm") == parse_units("g / (2.5 cm)")
    assert parse_units("g / 2.5cm") == parse_units("g / (2.5 cm)")
    assert parse_units("g / 25.mm") == parse_units("g / (25. mm)")
    assert parse_units("g / 2.5 * cm") == parse_units("g cm / 2.5")


def test_parse_unexpected():
    """Test that we cannot parse the units that we do not expect to."""
    unexpected = [
        "gibberish",
        5,
        "cp",  # Removed because of risk of collision with cP
        "chain",  # Survey units eliminated
        "SECONDS",  # Not just case insensitivity
        "lb : in^3",  # : is not a valid operator
    ]
    for unit in unexpected:
        with pytest.raises(UndefinedUnitError):
            parse_units(unit)

    scaling = [
        "3 rpm",  # No leading digits
        "16",  # No values that are just integers
        "16.2"  # No values that are just floats
    ]
    for unit in scaling:
        with pytest.raises(ValueError, match="scaling"):
            parse_units(unit)

    definition = [
        "/gram",  # A leading operator makes no sense
        "g / 0 m",  # Zero scaling factor
        "g / -2 m"  # Negative scaling factor
    ]
    for unit in definition:
        with pytest.raises(DefinitionSyntaxError):
            parse_units(unit)


def test_parse_none():
    """Test that None parses as None."""
    assert parse_units(None) is None


def test_format():
    """Test that custom formatting behaves as we hope."""
    # use the default unit registry for now
    reg = UnitRegistry(filename=pkg_resources.resource_filename("gemd.units", "citrine_en.txt"))

    result = parse_units("K^-2.0 m^-1e0 C^0 g^1 s^2")
    assert "-" not in result
    assert "[time]" in reg(result).dimensionality
    assert "[current]" not in reg(result).dimensionality
    kelvin = str(reg("K").units)
    gram = str(reg("g").units)
    second = str(reg("s").units)
    assert kelvin in result
    assert gram in result
    assert second in result
    assert result.index(gram) < result.index(kelvin)
    assert result.index(gram) < result.index(second)

    assert not re.search(r"\d", parse_units("m kg / s"))
    assert "/" not in parse_units("m kg s")
    assert "1" not in parse_units("s")
    assert "1" in parse_units("s^-1")
    assert "2.5" in parse_units("g / 2.5 cm")


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


def test_punctuation():
    """Test that punctuation parses reasonably."""
    assert parse_units('mol.') == parse_units('moles')
    assert parse_units('N.m') == parse_units('N * m')
    with pytest.raises(UndefinedUnitError):
        parse_units('mol : mol')
        import gemd.units
        print(gemd.units.impl._ALLOWED_OPERATORS)
