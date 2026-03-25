from enum import IntEnum
from contextlib import contextmanager
from logging import getLogger

__all__ = ["WarningLevel", "get_validation_level", "set_validation_level",
           "validation_level", "raise_or_warn"]

logger = getLogger(__name__)


class WarningLevel(IntEnum):
    """
    Control the behavior for warnings/errors around template validations.

    IGNORE: Do not check if values are consistent with bounds.
    WARNING: Accept bad values and issue a warning saying as much.
    FATAL: Raise an exception when trying to set an inconsistent value.

    """

    IGNORE = 0
    WARNING = 1
    FATAL = 2


BOUNDS_VALIDATION = WarningLevel.WARNING


def get_validation_level() -> WarningLevel:
    """Return the value of the BOUNDS_VALIDATION."""
    return BOUNDS_VALIDATION


def set_validation_level(level: WarningLevel):
    """Set the value of the BOUNDS_VALIDATION."""
    global BOUNDS_VALIDATION
    BOUNDS_VALIDATION = WarningLevel(level)


@contextmanager
def validation_level(level: WarningLevel):
    """Provide a context for setting a WarningLevel locally."""
    global BOUNDS_VALIDATION
    # Swap values and store
    old_value, BOUNDS_VALIDATION = BOUNDS_VALIDATION, WarningLevel(level)
    yield old_value  # Since we know the new level, the old one may be useful

    # Restore previous value
    BOUNDS_VALIDATION = old_value


def raise_or_warn(message, *, exc_class=ValueError, **kwargs):
    """Raise, warn, or ignore based on the current validation level.

    Parameters
    ----------
    message: str
        The error/warning message.
    exc_class: type
        Exception class to raise when level is FATAL.
    **kwargs:
        Additional keyword arguments passed to the exception constructor.

    """
    level = get_validation_level()
    if level == WarningLevel.IGNORE:
        return
    if level == WarningLevel.WARNING:
        logger.warning(message)
    else:
        raise exc_class(message, **kwargs)
