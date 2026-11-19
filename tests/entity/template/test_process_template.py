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


def test_allowed_names_removed():
    """Test that allowed_names warns of its removal and holds no value."""
    with pytest.warns(DeprecationWarning, match="allowed_names has been removed"):
        proc_template = ProcessTemplate(name="test template", allowed_names=["THF"])
    with pytest.warns(DeprecationWarning, match="allowed_names has been removed"):
        proc_template.allowed_names = ["Water"]
    with pytest.warns(DeprecationWarning, match="allowed_names has been removed"):
        assert proc_template.allowed_names == []
    assert "allowed_names" not in proc_template.as_dict()
    assert "allowed_names" not in dumps(proc_template)


def test_allowed_names_empty_warns():
    """Test that an empty allowed_names warns too, on the constructor and on the setter."""
    with pytest.warns(DeprecationWarning, match="allowed_names has been removed"):
        proc_template = ProcessTemplate(name="test template", allowed_names=[])
    with pytest.warns(DeprecationWarning, match="allowed_names has been removed"):
        proc_template.allowed_names = []
    with pytest.warns(DeprecationWarning, match="allowed_names has been removed"):
        proc_template.allowed_names = None


def test_allowed_names_omitted_does_not_warn():
    """Test that a template built without allowed_names emits no warning."""
    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        proc_template = ProcessTemplate(name="test template")
        assert loads(dumps(proc_template)) == proc_template
        ProcessTemplate.build({"type": "process_template", "name": "bare"})


@pytest.mark.parametrize("allowed_names", [[], ["batter"]])
def test_allowed_names_json_load(allowed_names):
    """Test that JSON with allowed_names loads with a warning and drops the field."""
    with pytest.warns(DeprecationWarning, match="allowed_names has been removed"):
        loaded = ProcessTemplate.build(
            {"type": "process_template", "name": "named", "allowed_names": allowed_names}
        )
    assert "allowed_names" not in loaded.as_dict()


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
