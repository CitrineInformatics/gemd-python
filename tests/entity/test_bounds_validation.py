import logging

import pytest

from gemd.entity.bounds_validation import WarningLevel, set_validation_level, \
    get_validation_level, validation_level, raise_or_warn


def test_bounds_validation():
    """Verify that changes to validation level behave as expected."""
    with validation_level(WarningLevel.IGNORE) as old_level:
        assert get_validation_level() == WarningLevel.IGNORE, "Context worked."
        set_validation_level(WarningLevel.WARNING)
        assert get_validation_level() == WarningLevel.WARNING, "Setter worked."
    assert get_validation_level() == old_level, "Original level restored."


def test_raise_or_warn_ignore():
    """Verify raise_or_warn does nothing at IGNORE level."""
    with validation_level(WarningLevel.IGNORE):
        raise_or_warn("should be ignored")  # no exception, no warning


def test_raise_or_warn_warning(caplog):
    """Verify raise_or_warn logs at WARNING level."""
    with validation_level(WarningLevel.WARNING):
        with caplog.at_level(logging.WARNING):
            raise_or_warn("check this")
    assert "check this" in caplog.text


def test_raise_or_warn_fatal():
    """Verify raise_or_warn raises at FATAL level."""
    with validation_level(WarningLevel.FATAL):
        with pytest.raises(ValueError, match="boom"):
            raise_or_warn("boom")
