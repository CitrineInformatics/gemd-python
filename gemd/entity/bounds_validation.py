from enum import IntEnum
from contextlib import contextmanager


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
