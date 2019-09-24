"""Test that units behave correctly."""
import pytest

from taurus.entity.value.nominal_real import NominalReal
from taurus.units import UndefinedUnitError


def test_units():
    """Make sure units can be set without error."""
    NominalReal(2.7, "")
    NominalReal(2.7, "cm")
    NominalReal(2.7, "cm^2/joule")
    NominalReal(2.7, "")


def test_invalid_units():
    """Make sure invalid units cause an error."""
    with pytest.raises(UndefinedUnitError):
        NominalReal(2.7, "hutch")
    with pytest.raises(ValueError):
        NominalReal(2.7)


def test_unit_normalization():
    """Make sure units are internally represented in a reasonable way."""
    assert NominalReal(2.7, "newton / m^2").units == NominalReal(2.7, "m^-1 newton / meter").units

    val = NominalReal(2.7, "cm")
    assert val.units == "centimeter"
    assert val.dump()["units"] == "centimeter"


def test_default_units():
    """An empty string should turn into the 'dimensionless' unit."""
    assert NominalReal(2.7, "") == NominalReal(2.7, "dimensionless")
