"""Tests of the ValidList class."""
import pytest
from taurus.entity.valid_list import ValidList


def test_access_data():
    """Test that valid data can be inserted into the list and that invalid data throws an error."""
    lo_strings = ValidList(['z'], str)
    lo_strings[0] = 'a'
    lo_strings.append('b')
    lo_strings.extend(tuple(['d', 'e', 'f']))
    lo_strings.insert(2, 'c')
    assert lo_strings == ['a', 'b', 'c', 'd', 'e', 'f']

    with pytest.raises(TypeError):
        ValidList(_list=tuple([1, 1]), content_type=1)
    with pytest.raises(TypeError):
        ValidList(_list=tuple([1, 1]), content_type=None)
    with pytest.raises(TypeError):
        lo_strings[0] = 1
    with pytest.raises(TypeError):
        lo_strings.append(1)
    with pytest.raises(TypeError):
        lo_strings.extend(tuple([1]))
    with pytest.raises(TypeError):
        lo_strings.insert(2, 1)

    lo_both = ValidList(_list=tuple([1, 'a']), content_type=[int, str])
    with pytest.raises(TypeError):
        lo_both[0] = 1.1


def test_triggers():
    """Tests that tiggers get fired off."""
    with pytest.raises(TypeError):
        ValidList(_list=tuple([1, 1]), content_type=int, trigger=1)

    stash = []

    def dummy(lst, val):
        stash.append(val)

    with pytest.raises(TypeError):
        ValidList(_list=tuple([1, 1]), trigger=dummy)

    vlst = ValidList(_list=tuple([1, 1]), content_type=int, trigger=dummy)
    vlst.append(1)
    vlst.extend([1])
    vlst.insert(2, 1)
    assert len(vlst) == 5
