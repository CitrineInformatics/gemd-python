"""Implementation of units."""
import re

from pint import UnitRegistry, Unit, register_unit_format, Quantity
from pint.compat import tokenizer
from tokenize import NAME, NUMBER, OP
# alias the error that is thrown when units are incompatible
# this helps to isolate the dependence on pint
from pint.errors import DimensionalityError as IncompatibleUnitsError  # noqa Import
from pint.errors import UndefinedUnitError, DefinitionSyntaxError  # noqa Import

import functools
import pkg_resources
from typing import Union

# use the default unit registry for now
DEFAULT_FILE = pkg_resources.resource_filename("gemd.units", "citrine_en.txt")
_ALLOWED_OPERATORS = {".", "+", "-", "*", "/", "//", "^", "**", "(", ")"}


def _scaling_preprocessor(input_string: str) -> str:
    """Preprocessor that turns scaling factors into non-dimensional units."""
    global _REGISTRY
    tokens = list(tokenizer(input_string))
    scales = []

    unrecognized = [t for t in tokens if t.type == OP and t.string not in _ALLOWED_OPERATORS]
    if len(unrecognized) > 0:
        raise UndefinedUnitError(f"Unrecognized operator(s): {unrecognized}")

    # Ignore leading numbers & operators, since Pint handles those itself
    start = next((i for i, token in enumerate(tokens) if token.type == NAME), len(tokens))

    for i, token in enumerate(tokens[start:], start=start):
        if token.type != NUMBER:
            continue

        # Note we can't run off the front because we started at a NAME
        first = i
        while tokens[first - 1].string in {'+', '-'}:
            first -= 1  # Include unary operations

        if tokens[first - 1].string in {"^", "**"}:
            continue  # Don't mangle exponents

        # Names couple tightly to their preceding numbers, so is it a denominator?
        division = tokens[first - 1].string in {"/", "//"}
        tight = i < len(tokens) - 2 and tokens[i + 1].type == NAME

        # Get the number
        substr = input_string[tokens[first].start[1]:token.end[1]]
        value = eval(substr)
        if value <= 0:
            raise DefinitionSyntaxError(f"Scaling factors must be positive: {substr}")
        scales.append([substr, token.string, division and tight])

    for substr, value, division in scales:
        # There's probably something to be said for stashing these, but this sin
        # should be ameliorated by the LRU cache
        regex = rf"(?<!=[-+0-9.]){re.escape(substr)}(?!=[0-9.])"
        valid = "_" + value.replace(".", "_").replace("+", "").replace("-", "_")
        trailing = "/" if division else ""
        _REGISTRY.define(f"{valid} = {value} = {value}")
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
        elif p > 0:
            numerator.append(f"{u} ** {p}")
        elif p == -1:
            denominator.append(u)
        elif p < 0:
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
        # TODO: parse_units has a bug resolved in 0.19, but 3.7 only supports up to 0.18
        parsed = _REGISTRY(units)
        if not isinstance(parsed, Quantity) or parsed.magnitude != 1:
            raise ValueError(f"Unit expression cannot have a leading scaling factor. {units}")
        return f"{parsed.u:clean}"
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
    _REGISTRY = UnitRegistry(filename=filename, preprocessors=[_scaling_preprocessor])
