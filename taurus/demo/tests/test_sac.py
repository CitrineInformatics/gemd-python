"""Test Strehlow & Cook demo."""
from taurus.demo.strehlow_and_cook import make_strehlow_table, make_strehlow_objects, \
    minimal_subset, import_table
import taurus.json as je


def test_sac():
    """Make S&C table and assert that it can be serialized."""
    sac = make_strehlow_objects(import_table())
    sac_tbl = make_strehlow_table(sac)

    # Check that all shapes of records serialize and deserialize
    for comp in sac:
        assert je.loads(je.dumps(comp)) == comp

    # Look at each different combination of Value types in a S&C record
    smaller = minimal_subset(sac_tbl['content'])
    # Make sure that the diversity of value types isn't lost, e.g. something is being None'd
    assert len(smaller) == 162

    # Make sure there's no migration with repeated serialization
    for row in sac_tbl:
        assert je.dumps(je.loads(je.dumps(row))) == je.dumps(row)
