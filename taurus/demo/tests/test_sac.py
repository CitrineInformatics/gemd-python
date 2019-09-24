"""Test Strehlow & Cook demo."""
from taurus.demo.strehlow_and_cook import make_strehlow_table, make_strehlow_objects
import taurus.client.json_encoder as je


def test_sac():
    """Make S&C table and assert that it can be serialized."""
    sac = make_strehlow_objects()
    sac_tbl = make_strehlow_table(sac)

    # Look at each different combination of Value types in a S&C record
    seen = set()
    for comp, row in zip(sac, sac_tbl['content']):
        mask = ''.join(map(lambda x: str(type(x)), row))
        if mask not in seen:
            seen.add(mask)
            # Check that all shapes of records serialize and deserialize
            assert je.loads(je.dumps(comp)) == comp
    # Make sure that the diversity of value types isn't lost, e.g. something is being None'd
    assert len(seen) == 12

    # Make sure there's no migration with repeated serialization
    assert je.dumps(je.loads(je.dumps(sac_tbl))) == je.dumps(sac_tbl)
