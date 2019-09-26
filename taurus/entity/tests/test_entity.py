"""General tests of entities."""
import pytest
from uuid import uuid4

from taurus.entity.attribute.condition import Condition
from taurus.entity.object.ingredient_run import IngredientRun
from taurus.entity.object.process_run import ProcessRun
from taurus.entity.value.nominal_real import NominalReal


def test_id_case_sensitivitiy():
    """Test that uids are case insensitive."""
    with pytest.raises(ValueError):
        ingredient = IngredientRun(uids={'my_id': 'sample1', 'My_ID': 'sample2'})

    ingredient = IngredientRun(uids={'my_id': 'sample1'})
    assert ingredient.uids['my_id'] == 'sample1'
    assert ingredient.uids['MY_id'] == 'sample1'


def test_content_hash():
    """Test that the content has is a string with all expected fields."""
    proc = ProcessRun("a process", uids={'id': str(uuid4())},
                      conditions=Condition("something", value=NominalReal(-10, '')))
    ingred = IngredientRun(name="ingredient", uids={'id': str(uuid4())},
                           absolute_quantity=NominalReal(3.5, 'g'), process=proc)
    ingred_hash = ingred.content_hash()
    assert isinstance(ingred_hash, str)
    assert 'absolute_quantity' in ingred_hash \
           and 'name' in ingred_hash \
           and 'uids' in ingred_hash \
           and 'process' in ingred_hash
