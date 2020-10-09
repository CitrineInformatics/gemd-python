"""Implementation of units."""
import pint
import pkg_resources
from typing import Union
from pint import UnitRegistry
from pint.unit import _Unit


# use the default unit registry for now
DEFAULT_FILE = pkg_resources.resource_filename("gemd.units", "citrine_en.txt")
_ureg = UnitRegistry(filename=DEFAULT_FILE)


# alias the error that is thrown when units are incompatible
# this helps to isolate the dependence on pint
IncompatibleUnitsError = pint.errors.DimensionalityError
UndefinedUnitError = pint.errors.UndefinedUnitError


def parse_units(units: Union[str, _Unit, None]) -> Union[str, _Unit, None]:
    """
    Parse a string or _Unit into a standard string representation of the unit.

    Parameters
    ----------
    units: Union[str, _Unit, None]
        The string or _Unit representation of the object we wish to display

    Returns
    -------
    [Union[str, _Unit, None]]
        The representation; note that the same type that was passed is returned

    """
    if units is None:
        return None
    elif units == '':
        return 'dimensionless'
    elif isinstance(units, str):
        return str(_ureg(units).units)
    elif isinstance(units, _Unit):
        return units
    else:
        raise UndefinedUnitError("Units must be given as a recognized unit string or Units object")


def convert_units(value: float, starting_unit: str, final_unit: str) -> float:
    """
    Convert the value from the starting_unit to the final_unit.

    Parameters
    ----------
    value: float
        magnitude to convert
    starting_unit: str
        unit that the magnitude is currently in
    final_unit: str
        unit that the magnitude should be returned in

    Returns
    -------
    [float]
        The converted number

    """
    return _ureg.Quantity(value, starting_unit).to(final_unit).magnitude


def change_definitions_file(filename: str = None):
    """
    Change which file is used for units definition.

    Parameters
    ----------
    filename: str
        The file to use

    """
    global _ureg
    if filename is None:
        filename = DEFAULT_FILE
    _ureg = UnitRegistry(filename=filename)
