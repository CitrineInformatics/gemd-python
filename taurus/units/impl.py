"""Implementation of units."""
import pint
import pkg_resources
from pint import UnitRegistry
from pint.quantity import _Quantity
from pint.unit import _Unit


# use the default unit registry for now
_ureg = UnitRegistry(filename=pkg_resources.resource_filename("taurus.units", "citrine_en.txt"))


# alias the error that is thrown when units are incompatible
# this helps to isolate the dependence on pint
IncompatibleUnitsError = pint.errors.DimensionalityError
UndefinedUnitError = pint.errors.UndefinedUnitError


def _unit_to_str(unit):
    """Helper that pulls a string representation of the unit from a quantity."""
    if not isinstance(unit, _Quantity):
        raise TypeError("Expecting a quantity")  # pragma: no cover
    return str(unit.units)


def parse_units(units):
    """Parse a string or _Unit into a standard string representation of the unit."""
    if units is None:
        return None
    elif units == '':
        return 'dimensionless'
    elif isinstance(units, str):
        return _unit_to_str(_ureg(units))
    elif isinstance(units, _Unit):
        return units
    else:
        raise UndefinedUnitError("Units must be given as a recognized unit string or Units object")


def convert_units(value, starting_unit, final_unit):
    """
    Convert the value from the starting_unit to the final_unit.

    :param value: magnitude to convert (number)
    :param starting_unit: unit that the magnitude is currently in (str)
    :param final_unit: unit that the magnitude should be returned in (str)
    """
    return _ureg.Quantity(value, starting_unit).to(final_unit).magnitude
