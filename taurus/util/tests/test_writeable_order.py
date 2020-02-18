import pytest

from taurus.entity.object import ProcessRun, MaterialRun
from taurus.entity.value.nominal_integer import NominalInteger
from taurus.util import writable_sort_order


def test_order_objects():
    """Test that sorting works when given objects."""
    unsorted = [MaterialRun("bar"), ProcessRun("foo")]
    sorted_list = sorted(unsorted, key=lambda x: writable_sort_order(x))

    assert isinstance(sorted_list[0], ProcessRun)
    assert isinstance(sorted_list[1], MaterialRun)


def test_order_strings():
    """Test that sorting works when given strings."""
    unsorted = [MaterialRun("bar"), ProcessRun("foo")]
    sorted_list = sorted(unsorted, key=lambda x: writable_sort_order(x.typ))

    assert isinstance(sorted_list[0], ProcessRun)
    assert isinstance(sorted_list[1], MaterialRun)


def test_sort_exception():
    """Test that value errors are raised when the input is invalid.

    Invalid inputs are non-base-entity objects and unrecognized type strings
    """
    with pytest.raises(ValueError):
        writable_sort_order("foo")

    with pytest.raises(ValueError):
        writable_sort_order(NominalInteger(2))
