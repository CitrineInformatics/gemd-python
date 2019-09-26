"""General tests of entities."""
import pytest

from taurus.entity.object.ingredient_run import IngredientRun


def test_id_case_sensitivitiy():
    """Test that uids are case insensitive."""
    with pytest.raises(ValueError):
        IngredientRun(uids={'my_id': 'sample1', 'My_ID': 'sample2'})

    ingredient = IngredientRun(uids={'my_id': 'sample1'})
    assert ingredient.uids['my_id'] == 'sample1'
    assert ingredient.uids['MY_id'] == 'sample1'
