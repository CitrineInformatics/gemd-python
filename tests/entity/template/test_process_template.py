"""Tests of the ProcessTemplate object."""

import warnings

import pytest

from gemd.entity.bounds import IntegerBounds
from gemd.entity.bounds.real_bounds import RealBounds
from gemd.entity.link_by_uid import LinkByUID
from gemd.entity.template.condition_template import ConditionTemplate
from gemd.entity.template.process_template import ProcessTemplate
from gemd.json import dumps, loads


def test_bounds_mismatch():
    """Test that a mismatch between the attribute and given bounds throws a ValueError."""
    attribute_bounds = RealBounds(0, 100, "")
    object_bounds = RealBounds(200, 300, "")
    cond_template = ConditionTemplate("a condition", bounds=attribute_bounds)
    with pytest.raises(ValueError):
        ProcessTemplate("a process template", conditions=[[cond_template, object_bounds]])


def test_allowed_names():
    """Test that allowed_names can be assigned, and that doing so warns of its deprecation."""
    allowed_names = ["THF", "Carbon Disulfide", "Dimethyl Ether"]
    with pytest.warns(DeprecationWarning, match="allowed_names"):
        proc_template = ProcessTemplate(name="test template", allowed_names=allowed_names)
    for name in allowed_names:
        assert name in proc_template.allowed_names

    with pytest.warns(DeprecationWarning, match="allowed_names"):
        proc_template.allowed_names = ["Water"]
    assert proc_template.allowed_names == ["Water"]


@pytest.mark.parametrize("allowed_names", [None, []])
def test_allowed_names_empty_does_not_warn(allowed_names):
    """Test that omitting allowed_names, or passing an empty list, emits no warning."""
    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        proc_template = ProcessTemplate(name="test template", allowed_names=allowed_names)
        assert proc_template.allowed_names == []
        assert ProcessTemplate(name="no names").allowed_names == []


def test_allowed_names_json_round_trip():
    """Test that JSON with and without allowed_names still loads and round-trips."""
    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        without_names = ProcessTemplate.build({"type": "process_template", "name": "bare"})
        assert without_names.allowed_names == []
        assert loads(dumps(without_names)).allowed_names == []

    with pytest.warns(DeprecationWarning, match="allowed_names"):
        with_names = ProcessTemplate.build(
            {"type": "process_template", "name": "named", "allowed_names": ["batter"]}
        )
    assert with_names.allowed_names == ["batter"]
    with pytest.warns(DeprecationWarning, match="allowed_names"):
        copied = loads(dumps(with_names))
    assert copied.allowed_names == ["batter"]


def test_allowed_labels():
    """Test that allowed_labels can be assigned.

    Presently allowed_labels is not used for any validation, but this test can be expanded
    if it is used in the future.
    """
    allowed_labels = ["solvent", "salt", "binder", "polymer"]
    proc_template = ProcessTemplate(name="test template", allowed_labels=allowed_labels)
    for label in allowed_labels:
        assert label in proc_template.allowed_labels


def test_passthrough_bounds():
    """Test that unspecified Bounds are accepted and set to None."""
    template = ProcessTemplate(
        "foo",
        conditions=[
            (LinkByUID("1", "2"), None),
            [LinkByUID("3", "4"), None],
            LinkByUID("5", "6"),
            ConditionTemplate("foo", bounds=IntegerBounds(0, 10)),
        ],
    )
    assert len(template.conditions) == 4
    for _, bounds in template.conditions:
        assert bounds is None
    copied = loads(dumps(template))
    assert len(copied.conditions) == 4
    for _, bounds in copied.conditions:
        assert bounds is None
    from_dict = ProcessTemplate.build(
        {
            "type": "process_template",
            "name": "foo",
            "conditions": [
                [
                    {
                        "scope": "foo",
                        "id": "bar",
                        "type": "link_by_uid",
                    },
                    None,
                ]
            ],
        }
    )
    assert len(from_dict.conditions) == 1


def test_dependencies():
    """Test that dependency lists make sense."""
    attribute_bounds = RealBounds(0, 100, "")
    cond_template = ConditionTemplate("a condition", bounds=attribute_bounds)
    proc_template = ProcessTemplate("a process template", conditions=[cond_template])
    assert cond_template in proc_template.all_dependencies()
