"""Tests of the ValidList class."""
import pytest

from gemd.entity.valid_list import ValidList


def test_access_data():
    """Test that valid data can be inserted into the list and that invalid data throws an error."""
    lo_strings = ValidList(['z'], str)
    lo_strings[0] = 'a'
    lo_strings.append('b')
    lo_strings.extend(tuple(['d', 'e', 'f']))
    lo_strings.insert(2, 'c')
    assert lo_strings == ['a', 'b', 'c', 'd', 'e', 'f']

    with pytest.raises(TypeError):
        lo_strings[0] = 1
    with pytest.raises(TypeError):
        lo_strings.append(1)
    with pytest.raises(TypeError):
        lo_strings.extend(tuple([1]))
    with pytest.raises(TypeError):
        lo_strings.extend(1)
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

    def dummy(val):
        stash.append(val)

    with pytest.raises(TypeError):
        ValidList(_list=tuple([1, 1]), trigger=dummy)

    vlst = ValidList(_list=tuple([1, 1]), content_type=int, trigger=dummy)
    vlst.append(1)
    vlst.extend([1])
    vlst.insert(2, 1)
    vlst[0] = 17
    assert len(vlst) == 5
    assert len(stash) == 6


def test_transform():
    """Test that transformations do what we expect in changing data."""
    first = [1, 2]
    vlst = ValidList(first,
                     content_type=int,
                     trigger=lambda x: x + 1)
    vlst.append(3)
    vlst.extend([4])
    vlst.insert(2, 5)
    assert vlst == [2, 3, 6, 4, 5]

    vlst[0] = 0
    assert vlst[0] == 1

    assert first == [1, 2]


def test_invalid_content():
    """Test that an invalid content_type throws a TypeError."""
    with pytest.raises(TypeError):
        ValidList(['z'], content_type={'types': [str]})
    with pytest.raises(TypeError):
        ValidList(_list=tuple([1, 1]), content_type=1)
    with pytest.raises(TypeError):
        ValidList(_list=tuple([1, 1]), content_type=None)
