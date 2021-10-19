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
