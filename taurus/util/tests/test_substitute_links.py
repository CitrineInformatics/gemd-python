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

    with pytest.raises(ValueError):
        substitute_links({mat: meas})


def test_object_key_substitution():
    """Test that client can copy a dictionary in which keys are BaseEntity objects."""
    spec = ProcessSpec("A process spec", uids={'id': str(uuid4()), 'auto': str(uuid4())})
    run1 = ProcessRun("A process run", spec=spec, uids={'id': str(uuid4())})
    run2 = ProcessRun("Another process run", spec=spec, uids={'id': str(uuid4())})
    process_dict = {spec: [run1, run2]}

    substitute_links(process_dict, native_uid='auto')
    for key, value in process_dict.items():
        assert key == LinkByUID.from_entity(spec, name='auto')
        assert LinkByUID.from_entity(run1) in value
        assert LinkByUID.from_entity(run2) in value
