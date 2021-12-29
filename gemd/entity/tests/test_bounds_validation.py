from gemd.entity.bounds_validation import WarningLevel, set_validation_level, \
    get_validation_level, validation_context


def test_bounds_validation():
    """Verify that changes to validation level behave as expected."""
    with validation_context(WarningLevel.IGNORE) as old_level:
        assert get_validation_level() == WarningLevel.IGNORE, "Context worked."
        set_validation_level(WarningLevel.WARNING)
        assert get_validation_level() == WarningLevel.WARNING, "Setter worked."
    assert get_validation_level() == old_level, "Original level restored."
