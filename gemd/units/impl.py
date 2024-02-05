"""Implementation of units."""
import functools
from importlib.resources import read_text
import os
from pathlib import Path
import re
from tempfile import TemporaryDirectory
from typing import Union, List, Tuple, Generator, Any

from pint import UnitRegistry, Unit, register_unit_format
try:  # Pint 0.23 migrated the location of this method, and augmented it
    from pint.pint_eval import tokenizer
except ImportError:  # pragma: no cover
    from pint.compat import tokenizer
from tokenize import NAME, NUMBER, OP, ERRORTOKEN, TokenInfo
# alias the error that is thrown when units are incompatible
# this helps to isolate the dependence on pint
from pint.errors import DimensionalityError as IncompatibleUnitsError  # noqa Import
from pint.errors import UndefinedUnitError, DefinitionSyntaxError  # noqa Import

# Store directories so they don't get auto-cleaned until exit
_TEMP_DIRECTORY = TemporaryDirectory()

__all__ = [
    "parse_units", "convert_units", "get_base_units", "change_definitions_file",
    "UndefinedUnitError", "IncompatibleUnitsError", "DefinitionSyntaxError"
]


def _deploy_default_files() -> str:
    """Copy the units & constants file into a temporary directory."""
    units_path = Path(_TEMP_DIRECTORY.name) / "citrine_en.txt"
    units_path.write_text(read_text("gemd.units", "citrine_en.txt"), encoding="utf-8")

    constants_path = Path(_TEMP_DIRECTORY.name) / "constants_en.txt"
    constants_path.write_text(read_text("gemd.units", "constants_en.txt"), encoding="utf-8")

    return str(units_path)


DEFAULT_FILE = _deploy_default_files()
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
    def _handle_operator(token_, exponent_context_, operator_stack_, result_):
        if token_.string not in _ALLOWED_OPERATORS:
            raise UndefinedUnitError(f"Unrecognized operator: {token_.string}")

        # Figure out what level to append at
        if exponent_context_ or token_.string in {"**", "^", ".", "-", "+"}:
            # Exponents & unaries do not change context
            result_[-1].append(token_)
        else:
            result_.append([])

        # Manage the operator stack
        if token_.string == '(':
            operator_stack_.append(token_)
        elif token_.string == ')':
            while operator_stack_:  # don't worry about enforcing balance
                if operator_stack_.pop().string == '(':
                    break  # We found token's friend
        elif token_.string in {"**", "^"}:
            # A spare to pop so next loop is in exponent context
            operator_stack_.extend([token_] * 2)

    def _handle_name(token_, exponent_context_, operator_stack_, result_):
        if exponent_context_ or len(result_[-1]) == 0 or result_[-1][-1].type != NAME:
            result_[-1].append(token_)
        else:  # Break blocks for two units in a row
            result_.append([token_])

    def _just_append(token_, exponent_context_, operator_stack_, result_):
        result_[-1].append(token_)

    def _do_nothing(token_, exponent_context_, operator_stack_, result_):
        pass

    dispatch = {
        OP: _handle_operator,
        NAME: _handle_name,
        NUMBER: _just_append,
        ERRORTOKEN: _just_append,
    }

    result = [[]]
    operator_stack = []
    for token in token_stream:
        exponent_context = any(t.string in {"**", "^"} for t in operator_stack)
        method = dispatch.get(token.type, _do_nothing)
        method(token, exponent_context, operator_stack, result)
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
            long_unit = f"{_REGISTRY.parse_units(stripped_unit)}"
            short_unit = f"{_REGISTRY.parse_units(stripped_unit):~}"
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


_REGISTRY: UnitRegistry = None  # global requires it be defined in this scope


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
        resolved_value = _REGISTRY.Quantity(value, starting_unit)
        resolved_final_unit = _REGISTRY.parse_units(final_unit)
        # Make sure count, radian, bit, and non-dimensional don't accidentally interconvert
        # https://pint.readthedocs.io/en/0.23/user/angular_frequency.html
        root1 = _REGISTRY.get_root_units(resolved_value)[1]
        root2 = _REGISTRY.get_root_units(resolved_final_unit)[1]
        if root1 != root2:
            raise IncompatibleUnitsError(
                units1=resolved_value.units,
                dim1=_REGISTRY.get_dimensionality(resolved_final_unit),
                units2=final_unit,
                dim2=_REGISTRY.get_dimensionality(resolved_final_unit)
            )
        return resolved_value.to(resolved_final_unit).magnitude


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
def parse_units(units: Union[str, Unit, None],
                *,
                return_unit: bool = False
                ) -> Union[str, Unit, None]:
    """
    Parse a string or Unit into a standard string representation of the unit.

    Parameters
    ----------
    units: str, Unit, or None
        The string or Unit representation of the object we wish to display
    return_unit: boolean
        Whether to return a pint Unit object, vs. whatever was initially passed

    Returns
    -------
    str, Unit, or None
        The representation; note that `return_unit` controls the return type

    """
    if units is None:
        if return_unit:
            return _REGISTRY.parse_units("")
        else:
            return None
    elif isinstance(units, str):
        parsed = _REGISTRY.parse_units(units)
        if return_unit:
            return parsed
        else:
            return f"{parsed:clean}"
    elif isinstance(units, Unit):
        return units
    else:
        raise UndefinedUnitError("Units must be given as a recognized unit string or Units object")


@functools.lru_cache(maxsize=1024)
def get_base_units(units: Union[str, Unit]) -> Tuple[Unit, float, float]:
    """
    Get the base units and conversion factors for the given unit.

    Parameters
    ----------
    units: str, Unit, or None
        The representation of the object we wish to display

    Returns
    -------
    Tuple[Unit, float, float]
        A tuple of the base unit, its multiplicative conversion factor, and its
        additive offset, in that order.

    """
    if isinstance(units, str):
        units = _REGISTRY.parse_units(units)
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
    parse_units.cache_clear()
    get_base_units.cache_clear()
    if filename is None:
        target = DEFAULT_FILE
    else:
        # TODO: Handle case where user provides a units file but no constants file
        target = Path(filename).expanduser().resolve(strict=True)

    current_dir = Path.cwd()
    try:
        path = Path(target)
        os.chdir(path.parent)
        # Need to re-verify path because of some slippiness around tmp on MacOS
        _REGISTRY = UnitRegistry(filename=Path.cwd() / path.name,
                                 preprocessors=[_space_after_minus_preprocessor,
                                                _scientific_notation_preprocessor,
                                                _scaling_preprocessor
                                                ],
                                 autoconvert_offset_to_baseunit=True
                                 )
    finally:
        os.chdir(current_dir)


change_definitions_file()  # initialize to default
