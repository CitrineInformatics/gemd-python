from gemd.entity.object import ProcessSpec, ProcessRun, MaterialSpec, MaterialRun
from gemd.entity.link_by_uid import LinkByUID
from gemd.util.impl import make_index


def test_make_index():
    """Test functionality of make_index method."""
    ps1 = ProcessSpec(name="hello", uids={"test_scope": "test_value"})
    pr1 = ProcessRun(
        name="world",
        spec=LinkByUID(scope="test_scope", id="test_value"),
        uids={"test_scope": "another_test_value"},
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
    gems = [ps1, pr1, ms1, mr1]
    gem_index = make_index(gems)
    assert ("test_scope", "test_value") in gem_index.keys()
    assert ("test_scope", "another_test_value") in gem_index.keys()
    assert ("second_scope", "this_is_an_id") in gem_index.keys()
    assert gem_index[("test_scope", "test_value")] == ps1
    assert gem_index[("test_scope", "another_test_value")] == pr1
    assert gem_index[("second_scope", "this_is_an_id")] == ms1
