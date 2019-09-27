"""Tests of the ProcessTemplate object."""
import pytest

from taurus.entity.template.process_template import ProcessTemplate
from taurus.entity.template.condition_template import ConditionTemplate
from taurus.entity.bounds.real_bounds import RealBounds


def test_bounds_mismatch():
    """Test that a mismatch between the attribute and given bounds throws a ValueError."""
    attribute_bounds = RealBounds(0, 100, '')
    object_bounds = RealBounds(200, 300, '')
    cond_template = ConditionTemplate("a condition", bounds=attribute_bounds)
    with pytest.raises(ValueError):
        ProcessTemplate("a process template", conditions=[[cond_template, object_bounds]])


def test_allowed_names():
    """
    Test that allowed_names can be assigned.

    Presently allowed_names is not used for any validation, but this test can be expanded
    if it is used in the future.
    """
    allowed_names = ["THF", "Carbon Disulfide", "Dimethyl Ether"]
    proc_template = ProcessTemplate(name="test template", allowed_names=allowed_names)
    for name in allowed_names:
        assert name in proc_template.allowed_names


def test_allowed_labels():
    """
    Test that allowed_labels can be assigned.

    Presently allowed_labels is not used for any validation, but this test can be expanded
    if it is used in the future.
    """
    allowed_labels = ["solvent", "salt", "binder", "polymer"]
    proc_template = ProcessTemplate(name="test template", allowed_labels=allowed_labels)
    for label in allowed_labels:
        assert label in proc_template.allowed_labels
