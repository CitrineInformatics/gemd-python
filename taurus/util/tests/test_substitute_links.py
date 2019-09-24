"""Test the substitute_links method, in particular the edge cases that the client doesn't test."""
import pytest
from uuid import uuid4

from taurus.util.impl import substitute_links
from taurus.entity.link_by_uid import LinkByUID
from taurus.entity.object import MeasurementRun, MaterialRun, ProcessRun, ProcessSpec


def test_substitution_without_id():
    """Test that trying to substitute links if uids haven't been assigned throws an error."""
    mat = MaterialRun("A material with no id")
    meas = MeasurementRun("A measurement with no id", material=mat)
    with pytest.raises(ValueError):
        substitute_links(meas), "substitute_links should fail if objects don't have uids"

    with pytest.raises(ValueError):
        substitute_links([meas, mat]), "substitute_links should fail if objects don't have uids"

    with pytest.raises(ValueError):
        substitute_links(meas.as_dict()), "substitute_links should fail if objects don't have uids"

    # Create a dictionary in which either the key or value is missing a uid
    meas.add_uid('id', str(uuid4()))
    with pytest.raises(ValueError):
        substitute_links({mat: meas}), "substitute_links should fail if objects don't have uids"
    with pytest.raises(ValueError):
        substitute_links({meas: mat}), "substitute_links should fail if objects don't have uids"


def test_native_id_substitution():
    """Test that the native id gets serialized, when specified."""
    native_id = 'id1'
    other_id = 'id2'
    # Create measurement and material with two ids
    mat = MaterialRun("A material", uids={native_id: str(uuid4()), other_id: str(uuid4())})
    meas = MeasurementRun("A measurement", material=mat,
                          uids={native_id: str(uuid4()), other_id: str(uuid4())})

    # Turn the material pointer into a LinkByUID using native_id
    substitute_links(meas, native_uid=native_id)
    assert meas.material == LinkByUID.from_entity(mat, name=native_id)

    # Put the measurement into a list and convert that into a LinkByUID using native_id
    measurements_list = [meas]
    substitute_links(measurements_list)
    assert measurements_list == [LinkByUID.from_entity(meas, name=native_id)]


def test_object_key_substitution():
    """Test that client can copy a dictionary in which keys are BaseEntity objects."""
    spec = ProcessSpec("A process spec", uids={'id': str(uuid4()), 'auto': str(uuid4())})
    run1 = ProcessRun("A process run", spec=spec, uids={'id': str(uuid4()), 'auto': str(uuid4())})
    run2 = ProcessRun("Another process run", spec=spec, uids={'id': str(uuid4())})
    process_dict = {spec: [run1, run2]}

    substitute_links(process_dict, native_uid='auto')
    for key, value in process_dict.items():
        assert key == LinkByUID.from_entity(spec, name='auto')
        assert LinkByUID.from_entity(run1, name='auto') in value
        assert LinkByUID.from_entity(run2) in value

    reverse_process_dict = {run2: spec}
    substitute_links(reverse_process_dict, native_uid='auto')
    for key, value in reverse_process_dict.items():
        assert key == LinkByUID.from_entity(run2)
        assert value == LinkByUID.from_entity(spec, name='auto')
