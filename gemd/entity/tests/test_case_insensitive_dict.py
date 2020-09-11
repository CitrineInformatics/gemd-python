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


def test_all_dict_methods():
    """Tests checking consistency of all standard dictionary methods."""
    # __init__
    data = {'K' + x: 'V' + x for x in ('1', '2', '3', '4', '5')}
    ci_dict = CaseInsensitiveDict(**data)

    assert sorted(list(ci_dict)) == sorted(list(data))
    assert len(ci_dict) == len(data)

    # __getitem__
    assert ci_dict['K1'] == data['K1']

    # __setitem__
    ci_dict['K6'] = 'V6'
    assert ci_dict['K6'] == 'V6'

    # __delitem__
    del ci_dict['K6']
    assert 'K6' not in ci_dict

    # iter(d)
    ci_iter = iter(ci_dict)
    for k in ci_iter:
        assert k in data

    # clear
    ci_dict.clear()
    assert len(ci_dict) == 0
    assert len(ci_dict.lowercase_dict) == 0
    for k, v in data.items():
        ci_dict[k.lower()] = v.lower()

    # copy
    dup = ci_dict.copy()
    assert type(dup) == type(ci_dict)

    # fromkeys
    key_copy = CaseInsensitiveDict.fromkeys(dup)
    assert set(dup) == set(key_copy)
    assert type(dup) == type(key_copy)

    # get
    assert ci_dict.get('K1') == 'v1'
    assert ci_dict.get('K6', None) is None

    # items
    for k, v in ci_dict.items():
        assert data[k.upper()] == v.upper()

    # keys
    for k in ci_dict.keys():
        assert k not in data  # because the cases are all wrong

    # pop
    assert ci_dict.pop('k1') == 'v1'
    assert 'K1' not in ci_dict
    with pytest.raises(KeyError):
        ci_dict.pop('k1')
    assert ci_dict.pop('k1', None) is None

    # popitem
    pop_k, pop_v = ci_dict.popitem()
    assert pop_k not in ci_dict

    # setdefault
    assert ci_dict.setdefault(pop_k.upper(), pop_v.upper()) == pop_v.upper()
    assert ci_dict.setdefault(pop_k.upper(), pop_v.lower()) == pop_v.upper()

    # update
    ci_dict.update({pop_k.upper(): pop_v.lower(), 'K6': 'v6'})
    ci_dict.update(K6='V6')
    with pytest.raises(ValueError):
        ci_dict.update(k6='v6')
    with pytest.raises(ValueError):
        ci_dict.update({k.lower(): v for k, v in ci_dict.items()})

    # values
    assert 'V6' in ci_dict.values()
