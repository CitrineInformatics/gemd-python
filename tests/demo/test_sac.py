"""Test Strehlow & Cook demo."""
from gemd.demo.strehlow_and_cook import make_strehlow_table, make_strehlow_objects, \
    minimal_subset, import_table
import gemd.json as gemd_json
import json as json_builtin


def test_sac():
    """Make S&C table and assert that it can be serialized."""
    sac = make_strehlow_objects(import_table())
    sac_tbl = make_strehlow_table(sac)

    # Check that all shapes of records serialize and deserialize
    for comp in sac:
        assert gemd_json.loads(gemd_json.dumps(comp)) == comp

    # Verify that specs are shared when compounds match
    for comp1 in sac:
        for comp2 in sac:
            # xand
            assert (comp1.name == comp2.name) == (comp1.spec.uids == comp2.spec.uids)

    # Look at each different combination of Value types in a S&C record
    smaller = minimal_subset(sac_tbl['content'])
    # Make sure that the diversity of value types isn't lost, e.g. something is being None'd
    assert len(smaller) == 162

    # Make sure there's no migration with repeated serialization
    for row in sac_tbl:
        assert gemd_json.dumps(gemd_json.loads(gemd_json.dumps(row))) == gemd_json.dumps(row)

    # Verify that the serialization trick for mocking a structured table works
    json_builtin.dumps(json_builtin.loads(gemd_json.dumps(sac_tbl))["object"], indent=2)
