"""Tests of the case-insensitive dictionary class."""
import pytest

from gemd.entity.case_insensitive_dict import CaseInsensitiveDict
from gemd.entity.object.process_run import ProcessRun
from gemd.json import loads, dumps


def test_case_sensitivity():
    """Test some basic setting and getting operations."""
    # If two keys are the same up to case, the dictionary is invalid.
    bad_data = {'A': 1, 'a': 2}
    with pytest.raises(ValueError):
        CaseInsensitiveDict(**bad_data)

    data = {'key1': 'value1', 'key2': 2}
    data_dict = CaseInsensitiveDict(**data)
    data_dict['kEY3'] = "three"  # A new key-value pair can be added.
    data_dict['key2'] = 22  # An existing can be overridden by the exact same key.

    # A value can be accessed by the key, no matter what the case is.
    assert data_dict['key2'] == 22
    assert data_dict['KEY2'] == 22
    assert data_dict.get('KEY2') == 22

    # A failed get with a default value is not fatal
    with pytest.raises(KeyError):
        data_dict['KEY4'] == 4
    data_dict.get('Key4', 4) == 4

    # Check that the keys maintain their original case
    assert set(data_dict.keys()) == {'key1', 'key2', 'kEY3'}

    # A value cannot be overridden by a key that is similar but has different case.
    # If the user has defined an id with scope 'my_id' they shouldn't be setting 'My_ID'.
    with pytest.raises(ValueError):
        data_dict['KEY2'] = 222

    # A bad assignment attempt should not alter the dictionary
    assert data_dict['KEY2'] == 22


def test_serde():
    """Test that an object with a case-insensitive dict can be serialized properly."""
    process = ProcessRun("A process", uids={'Foo': str(17)})
    process_copy = loads(dumps(process))
    assert process == process_copy
    assert process_copy.uids['foo'] == process_copy.uids['Foo']


def test_contains():
    """Test checking whether or not a case insensitive dict contains a key."""
    data = {'Key': 'value'}
    data_dict = CaseInsensitiveDict(**data)
    for k in ('key', 'Key', 'KEY'):
        assert k in data_dict

    assert 'not_a_key' not in data_dict
