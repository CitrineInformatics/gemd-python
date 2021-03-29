from gemd.entity.object import ProcessSpec, ProcessRun, MaterialSpec, MaterialRun
from gemd.entity.link_by_uid import LinkByUID
from gemd.util.impl import make_index, substitute_objects


def test_make_index():
    """Test functionality of make_index method."""
    ps1 = ProcessSpec(name="hello", uids={"test_scope": "test_value"})
    pr1 = ProcessRun(
        name="world",
        spec=LinkByUID(scope="test_scope", id="test_value"),
        uids={"test_scope": "another_test_value",
              "other_test": "also_valid"
              },
    )
    ms1 = MaterialSpec(
        name="material",
        process=LinkByUID(scope="test_scope", id="test_value"),
        uids={"second_scope": "this_is_an_id"},
    )
    mr1 = MaterialRun(
        name="material_run",
        spec=LinkByUID(scope="second_scope", id="this_is_an_id"),
        process=LinkByUID(scope="test_scope", id="another_test_value"),
    )

    pr2 = ProcessRun(
        name="goodbye",
        spec=LinkByUID.from_entity(ps1),
        uids={"test_scope": "the_other_value"},
    )
    mr2 = MaterialRun(
        name="cruel",
        spec=LinkByUID.from_entity(ms1),
        process=LinkByUID.from_entity(pr2),
    )

    gems = [ps1, pr1, ms1, mr1, pr2, mr2]
    gem_index = make_index(gems)
    for gem in gems:
        for scope in gem.uids:
            assert (scope, gem.uids[scope]) in gem_index
            assert gem_index[(scope, gem.uids[scope])] == gem

    # Make sure substitute_objects can consume the index
    subbed = substitute_objects(mr1, gem_index)
    assert subbed.spec.uids == ms1.uids
