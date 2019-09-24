"""Test the substitute_links method, in particular the edge cases that the client doesn't test."""
import pytest

from taurus.util.impl import substitute_links
from taurus.entity.object.measurement_run import MeasurementRun
from taurus.entity.object.material_run import MaterialRun


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
