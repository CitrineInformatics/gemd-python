"""Implementation of units."""
import re

from pint import UnitRegistry, Unit, register_unit_format
from pint.compat import tokenizer
from tokenize import NAME, NUMBER, OP, ERRORTOKEN, TokenInfo
# alias the error that is thrown when units are incompatible
# this helps to isolate the dependence on pint
from pint.errors import DimensionalityError as IncompatibleUnitsError  # noqa Import
from pint.errors import UndefinedUnitError, DefinitionSyntaxError  # noqa Import

import functools
import pkg_resources
from typing import Union, List, Tuple, Generator, Any

# use the default unit registry for now
DEFAULT_FILE = pkg_resources.resource_filename("gemd.units", "citrine_en.txt")
_ALLOWED_OPERATORS = {".", "+", "-", "*", "/", "//", "^", "**", "(", ")"}


def _space_after_minus_preprocessor(input_string: str) -> str:
    """A preprocessor that protects against a pint < 0.21 bug."""
    return re.sub(r"(?<=-)\s+(?=\d)", "", input_string)


def _scientific_notation_preprocessor(input_string: str) -> str:
    """Preprocessor that converts x * 10 ** y format to xEy."""
    def _as_scientific(matchobj: re.Match) -> str:
        return f"{matchobj.group(1) or '1'}e{matchobj.group(2)}"

    number = r'\b(?:(\d+\.?\d*|\.\d+)\s*\*\s*)?10\s*(?:\*{2}|\^)\s*\+?(-?\d+\b)'
    return re.sub(number, _as_scientific, input_string)


def _scaling_find_blocks(token_stream: Generator[TokenInfo, Any, None]) -> List[List[TokenInfo]]:
    """
    Supporting routine for _scaling_preprocessor; tokenizer stream -> blocks.

    Takes a stream of tokens, and breaks it into a lists of tokens that represent
    multiplicative subunits of the original expression.

    """
    result = [[]]
    operator_stack = []
    for token in token_stream:
        exponent_context = any(t.string in {"**", "^"} for t in operator_stack)
        if token.type == OP:
            if token.string not in _ALLOWED_OPERATORS:
                raise UndefinedUnitError(f"Unrecognized operator: {token.string}")

            if exponent_context or token.string in {"**", "^", ".", "-", "+"}:
                # Exponents & unaries do not change context
                result[-1].append(token)
            elif token.string not in {}:
                result.append([])

            if token.string == '(':
                operator_stack.append(token)
            elif token.string == ')':
                while operator_stack:  # don't worry about enforcing balance
                    if operator_stack.pop().string == '(':
                        break  # We found token's friend
            elif token.string in {"**", "^"}:
                operator_stack.append(token)
                continue  # Break flow since next token is in exponent context
        elif token.type == NAME:
            if exponent_context or len(result[-1]) == 0 or result[-1][-1].type != NAME:
                result[-1].append(token)
            else:  # Break blocks for two units in a row
                result.append([token])
        elif token.type == NUMBER:
            result[-1].append(token)
        elif token.type == ERRORTOKEN:  # Keep non-legal Python symbols like °
            result[-1].append(token)
        # Drop other tokens, such as EOF

        if len(operator_stack) > 0 and operator_stack[-1].string in {"**", "^"}:
            operator_stack.pop()  # Exit context for this exponential

    return result


def _scaling_identify_factors(
        input_string: str,
        blocks: List[List[TokenInfo]]
) -> List[Tuple[str, str, str]]:
    """
    Supporting routine for _scaling_preprocessor; blocks -> scaling terms.

    Takes the input_string and the blocks output by _scaling_find_blocks and
    returns a tuple of the substrings that contain scaling factors, the scaling
    factor itself, and the unit string.

    """
    todo = []
    for block in blocks:
        i_exp = next((i for i, t in enumerate(block) if t.string in {"**", "^"}), len(block))
        i_name = next((i for i, t in enumerate(block) if t.type == NAME), None)
        numbers = [(i, t.string) for i, t in enumerate(block) if t.type == NUMBER and i < i_exp]

        if len(numbers) == 1:
            position, value = numbers[0]
            if i_exp != len(block):
                raise ValueError(
                    f"Scaling factors ({value}) with exponents are not supported ({input_string})"
                )
            if i_name is not None and i_name < position:
                raise ValueError(f"Scaling factor ({value}) follows unit in {input_string}")
            if float(value) != 1.0 and float(value) != 0.0:  # Don't create definitions for 0 or 1
                block_string = input_string[block[0].start[1]:block[-1].end[1]]
                if i_name is None:
                    unit_string = None
                else:
                    unit_string = input_string[block[position + 1].start[1]:block[i_name].end[1]]
                todo.append((block_string, value, unit_string))
        elif len(numbers) > 1:
            raise ValueError(
                f"Replicate scaling factor ({[n[1] for n in numbers]}) in {input_string}"
            )

    return todo


def _scaling_store_and_mangle(input_string: str, todo: List[Tuple[str, str, str]]) -> str:
    """
    Supporting routine for _scaling_preprocessor; scaling terms -> updated input_string.

    Takes the terms to be updated, and actually updates the input_string as well as
    creating an entry for each in the registry.

    """
    for scaled_term, number_string, unit_string in todo:
        regex = rf"(?<![-+0-9.]){re.escape(scaled_term)}(?![0-9.])"
        stripped = re.sub(r"[+\s]+", "", scaled_term).replace("--", "")

        if unit_string is not None:
            stripped_unit = re.sub(r"[+\s]+", "", unit_string).replace("--", "")
            long_unit = f"{_REGISTRY(stripped_unit).u}"
            short_unit = f"{_REGISTRY(stripped_unit).u:~}"
            long = stripped.replace(stripped_unit, "_" + long_unit)
            short = stripped.replace(stripped_unit, " " + short_unit)
        else:
            long = stripped
            short = stripped

        underscored = re.sub(r"[-.]", "_", long)
        valid = f"_{underscored}"
        if valid not in _REGISTRY:
            # Parse subexpression to clean things up for define
            value = f"{_REGISTRY.parse_expression(scaled_term)}"
            _REGISTRY.define(f"{valid} = {value} = {short}")
        input_string = re.sub(regex, valid, input_string)

    return input_string


def _scaling_preprocessor(input_string: str) -> str:
    """Preprocessor that turns scaling factors into non-dimensional units."""
    blocks = _scaling_find_blocks(tokenizer(input_string))

    blocks.pop(0)  # Leading term is not allowed to be a scaling factor
    todo = _scaling_identify_factors(input_string, blocks)

    return _scaling_store_and_mangle(input_string, todo)


_REGISTRY = UnitRegistry(filename=DEFAULT_FILE,
                         preprocessors=[_space_after_minus_preprocessor,
                                        _scientific_notation_preprocessor,
                                        _scaling_preprocessor],
                         autoconvert_offset_to_baseunit=True)


@register_unit_format("clean")
def _format_clean(unit, registry, **options):
    """Formatter that turns scaling-factor-units into numbers again."""
    numerator = []
    denominator = []
    for u, p in unit.items():
        if re.match(r"_[\d_]+", u):
            # Munged scaling factor; grab symbol, which is the prettier
            u = registry.get_symbol(u)

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
def _parse_units(units: str) -> Unit:
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
    # TODO: parse_units has a bug resolved in 0.19, but 3.7 only supports up to 0.18
    parsed = _REGISTRY(units)
    try:
        magnitude = parsed.magnitude
        result = parsed.units
    except AttributeError:  # It was non-dimensional
        magnitude = parsed
        result = _REGISTRY("").u
    if magnitude == 0.0:
        raise ValueError(f"Unit expression had a zero scaling factor. {units}")
    if magnitude != 1:
        raise ValueError(f"Unit expression cannot have a leading scaling factor. {units}")
    return result


def parse_units(units: Union[str, Unit, None],
                *,
                return_unit: bool = False
                ) -> Union[str, Unit, None]:
    """
    Parse a string or Unit into a standard string representation of the unit.

    Parameters
    ----------
    units: Union[str, Unit, None]
        The string or Unit representation of the object we wish to display
    return_unit: boolean
        Whether to return a Unit object, vs. whatever was initially passed

    Returns
    -------
    [Union[str, Unit, None]]
        The representation; note that the same type that was passed is returned

    """
    if units is None:
        if return_unit:
            return _REGISTRY("").u
        else:
            return None
    elif isinstance(units, str):
        parsed = _parse_units(units)
        if return_unit:
            return parsed
        else:
            return f"{parsed:clean}"
    elif isinstance(units, Unit):
        return units
    else:
        raise UndefinedUnitError("Units must be given as a recognized unit string or Units object")


@functools.lru_cache(maxsize=1024 * 1024)
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
        resolved_final_unit = _REGISTRY(final_unit).u  # `to` bypasses preparser
        return _REGISTRY.Quantity(value, starting_unit).to(resolved_final_unit).magnitude


@functools.lru_cache(maxsize=1024)
def get_base_units(units: Union[str, Unit]) -> Tuple[Unit, float, float]:
    """
    Get the base units and conversion factors for the given unit.

    Parameters
    ----------
    units: Union[str, Unit, None]
        The string or Unit representation of the object we wish to display

    Returns
    -------
    Tuple[Unit, Number, float]
        The base unit, its

    """
    if isinstance(units, str):
        units = _REGISTRY(units).u
    ratio, base_unit = _REGISTRY.get_base_units(units)
    offset = _REGISTRY.Quantity(0, units).to(_REGISTRY.Quantity(0, base_unit)).magnitude
    return base_unit, float(ratio), offset


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
    _REGISTRY = UnitRegistry(filename=filename,
                             preprocessors=[
                                 _space_after_minus_preprocessor,
                                 _scientific_notation_preprocessor,
                                 _scaling_preprocessor
                             ],
                             autoconvert_offset_to_baseunit=True)
