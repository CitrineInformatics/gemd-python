"""Implementation of units."""
import re

from pint import UnitRegistry, Unit, register_unit_format
from pint.compat import tokenizer
from tokenize import NAME, NUMBER, OP
# alias the error that is thrown when units are incompatible
# this helps to isolate the dependence on pint
from pint.errors import DimensionalityError as IncompatibleUnitsError  # noqa Import
from pint.errors import UndefinedUnitError

import functools
import pkg_resources
from typing import Union

# use the default unit registry for now
DEFAULT_FILE = pkg_resources.resource_filename("gemd.units", "citrine_en.txt")


def _scaling_preprocessor(input_string: str) -> str:
    """Preprocessor that turns scaling factors into non-dimensional units."""
    global _REGISTRY
    tokens = tokenizer(input_string)
    exponent = False
    division = False
    tight_division = False
    scales = []

    for token in tokens:
        # Note that while this prevents adding a bunch of numbers to the registry,
        # no test would break if the `exponent` logic were removed
        if tight_division:
            # A unit for a scaling factor is in the denominator if the factor is
            scales[-1][-1] = token.type == NAME
            tight_division = False
        if not exponent and token.type == NUMBER:
            scales.append([token.string, False])
            tight_division = division
        exponent = token.type == OP and token.string in {"^", "**"}
        division = token.type == OP and token.string in {"/", "//"}

    for scale, division in scales:
        # There's probably something to be said for stashing these, but this sin
        # should be ameliorated by the LRU cache
        regex = rf"\b{re.escape(scale)}(?!=[0-9.])"
        valid = "_" + scale.replace(".", "_").replace("+", "").replace("-", "_")
        trailing = "/" if division else ""
        _REGISTRY.define(f"{valid} = {scale} = {scale}")
        input_string = re.sub(regex, valid + trailing, input_string)

    return input_string


_REGISTRY = UnitRegistry(filename=DEFAULT_FILE, preprocessors=[_scaling_preprocessor])


@register_unit_format("clean")
def _format_clean(unit, registry, **options):
    """Formatter that turns scaling-factor-units into numbers again."""
    numerator = []
    denominator = []
    for u, p in unit.items():
        if re.match(r"_[\d_]+$", u):
            # Munged scaling factor; drop leading underscore, restore . and -
            u = re.sub(r"(?<=\d)_(?=\d)", ".", u[1:]).replace("_", "-")

        if p == 1:
            numerator.append(u)
        elif p > 1:
            numerator.append(f"{u} ** {p}")
        elif p == -1:
            denominator.append(u)
        elif p < -1:
            denominator.append(f"{u} ** {-p}")

    if len(numerator) == 0:
        numerator = ["1"]

    if len(denominator) > 0:
        return " / ".join((" * ".join(numerator), " / ".join(denominator)))
    else:
        return " * ".join(numerator)


@functools.lru_cache(maxsize=1024)
def parse_units(units: Union[str, Unit, None]) -> Union[str, Unit, None]:
    """
    Parse a string or Unit into a standard string representation of the unit.

    Parameters
    ----------
    units: Union[str, Unit, None]
        The string or Unit representation of the object we wish to display

    Returns
    -------
    [Union[str, Unit, None]]
        The representation; note that the same type that was passed is returned

    """
    if units is None:
        return None
    elif units == '':
        return 'dimensionless'
    elif isinstance(units, str):
        return f"{_REGISTRY(units).u:clean}"
    elif isinstance(units, Unit):
        return units
    else:
        raise UndefinedUnitError("Units must be given as a recognized unit string or Units object")


@functools.lru_cache(maxsize=None)
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
    if starting_unit == final_unit:
        return value  # skip computation
    else:
        return _REGISTRY.Quantity(value, starting_unit).to(final_unit).magnitude


def change_definitions_file(filename: str = None):
    """
    Change which file is used for units definition.

    Parameters
    ----------
    filename: str
        The file to use

    """
    global _REGISTRY
    convert_units.cache_clear()  # Units will change
    if filename is None:
        filename = DEFAULT_FILE
    _REGISTRY = UnitRegistry(filename=filename)
