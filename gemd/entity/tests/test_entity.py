"""General tests of entities."""
import pytest

from gemd.entity.object.ingredient_run import IngredientRun
from gemd.entity.link_by_uid import LinkByUID


def test_id_case_sensitivitiy():
    """Test that uids are case insensitive."""
    with pytest.raises(ValueError):
        IngredientRun(uids={'my_id': 'sample1', 'My_ID': 'sample2'})

    ingredient = IngredientRun(uids={'my_id': 'sample1'})
    assert ingredient.uids['my_id'] == 'sample1'
    assert ingredient.uids['MY_id'] == 'sample1'


def test_to_link():
    """Test that to_link behaves as expected."""
    obj = IngredientRun(uids={"Scope": "UID", "Second": "option"})
    assert isinstance(obj.to_link(), LinkByUID), "Returns a useful LinkByUID"
    assert LinkByUID(scope="Scope", id="UID") == obj.to_link("Scope"), "Correct choice of UID"

    with pytest.raises(ValueError):
        IngredientRun().to_link(), "to_link on an object w/o IDs is fatal"

    with pytest.raises(ValueError):
        obj.to_link("Third"), "to_link with a scope that an object lacks is fatal"

    assert obj.to_link(scope="Third", allow_fallback=True).scope in obj.uids, \
        "... unless allow_fallback is set"


def test_equality():
    """Test that __eq__ and _cached_equals behave as expected."""
    from gemd.entity.object import ProcessSpec, IngredientSpec, MaterialSpec
    from gemd.entity.link_by_uid import LinkByUID

    one = ProcessSpec("Object", tags=["tags!"], uids={"scope": "id"})
    assert one == LinkByUID(scope="scope", id="id"), "Objects equal their links"
    assert one == ("scope", "id"), "Objects equal their equivalent tuples"
    assert one != ("scope", "id", "extra"), "But not if they are too long"
    assert one != ("epocs", "id"), "Or have the wrong scope"
    assert one != ("scope", "di"), "Or have the wrong id"

    junk = MaterialSpec("Object", tags=["tags!"], uids={"scope": "id"})
    assert one != junk, "Objects don't match across types"

    two = ProcessSpec("Object", tags=["tags!"], uids={"scope": "id"}, notes="Notes!")
    assert one != two, "Objects don't match unless the fields do"
    one.notes = "Notes!"
    assert one == two, "And then they will"

    # It ignores the ingredient length mismatch if the uids matched
    one_ing = IngredientSpec("Ingredient", process=one)
    assert one == two
    assert two == one

    # And a cycle is not a problem
    one_mat = MaterialSpec("Material", tags=["other tags!"], process=one)
    two_mat = MaterialSpec("Material", tags=["other tags!"], process=two)
    one_ing.material = one_mat
    two_ing = IngredientSpec("Ingredient", process=one, material=one_mat)
    assert one == two
    assert two == one

    # Order doesn't matter for tags
    one.tags = ["One", "Two", "Three", "Four"]
    two.tags = ["Four", "One", "Three", "Two"]
    assert one == two
    assert two == one

