import pytest

from taurus.entity.source.performed_source import PerformedSource


def test_construction():
    """Make sure we can and cannot construct correct and incorrect performed sources."""
    PerformedSource()
    PerformedSource(performed_by="Marie Curie")
    PerformedSource(performed_date="1898-07-01")
    PerformedSource(performed_date="1898-07-01", performed_by="Marie Curie")

    with pytest.raises(TypeError):
        PerformedSource(performed_date=1234)

    with pytest.raises(TypeError):
        PerformedSource(performed_by={"first_name": "Marie", "last_name": "Curie"})

    with pytest.raises(ValueError):
        PerformedSource(performed_date="The Ides of March")
