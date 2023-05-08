"""General tests of entities."""
from abc import ABC
import inspect
import pytest
from typing import Generic, TypeVar

from gemd import ProcessSpec, IngredientSpec, MaterialSpec, IngredientRun, \
    LinkByUID, ConditionTemplate, MolecularStructureBounds
from gemd.entity.dict_serializable import DictSerializable
from gemd.entity.base_entity import BaseEntity


def test_id_case_sensitivity():
    """Test that uids are case-insensitive."""
    with pytest.raises(ValueError):
        IngredientRun(uids={'my_id': 'sample1', 'My_ID': 'sample2'})

    ingredient = IngredientRun(uids={'my_id': 'sample1'})
    assert ingredient.uids['my_id'] == 'sample1'
    assert ingredient.uids['MY_id'] == 'sample1'


def test_id_iterables():
    """Test that the uids setter is very forgiving."""
    assert IngredientRun(uids={'my_id': 'sample1'}).uids['my_id'] == 'sample1'
    assert IngredientRun(uids=['my_id', 'sample1']).uids['my_id'] == 'sample1'
    assert IngredientRun(uids=('my_id', 'sample1')).uids['my_id'] == 'sample1'


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
    one_ing.material = two_mat
    IngredientSpec("Ingredient", process=two, material=one_mat)  # two_ing
    assert one == two
    assert two == one

    # Order doesn't matter for tags
    one.tags = ["One", "Two", "Three", "Four"]
    two.tags = ["Four", "One", "Three", "Two"]
    assert one == two
    assert two == one


@pytest.mark.xfail(reason="Entities fail the isabstract test.")
def test_meta_behaviors():  # pragma: no cover
    """Test the DictSerializable metaclass behaviors."""
    assert inspect.isabstract(BaseEntity)
    with pytest.raises(TypeError, match="DictSerializable"):
        BaseEntity(uids={}, tags=[])

    child_typ = "child_entity"
    child_skip = "field"

    class ChildEntity(BaseEntity, typ=child_typ, skip={child_skip}):
        pass

    assert not inspect.isabstract(ChildEntity)
    obj = ChildEntity(uids={}, tags=[])

    assert ChildEntity.typ == child_typ
    assert obj.typ == child_typ
    assert BaseEntity.typ != child_typ
    assert child_skip in ChildEntity.skip
    assert child_skip in obj.skip
    assert child_skip not in BaseEntity.skip


def test_meta_behaviors_limited():
    """Test the DictSerializable metaclass behaviors."""
    child_typ = "child_entity"
    child_skip = "field"

    class ChildEntity(BaseEntity, typ=child_typ, skip={child_skip}):
        pass

    obj = ChildEntity(uids={}, tags=[])

    assert ChildEntity.typ == child_typ
    assert obj.typ == child_typ
    assert BaseEntity.typ != child_typ
    assert child_skip in ChildEntity.skip
    assert child_skip in obj.skip
    assert child_skip not in BaseEntity.skip


def test_mro():
    """This test mimics a citrine-python class inheritance structure."""
    SerializableType = TypeVar('SerializableType', bound='Serializable')
    ResourceType = TypeVar('ResourceType', bound='Resource')

    class Serializable(Generic[SerializableType]):
        pass

    class Resource(Serializable[ResourceType]):
        pass

    class DataConcepts(DictSerializable, Serializable['DataConcepts'], ABC):
        pass

    class TestConditionTemplate(
        DataConcepts,
        Resource['TestConditionTemplate'],
        ConditionTemplate
    ):
        pass

    TestConditionTemplate(name="Me", bounds=MolecularStructureBounds())


def test_derived_collision():
    """Test that an exception is thrown when multiple classes claim the same typ."""
    # One parent
    class Parent(DictSerializable, typ="mine"):
        pass

    # First kid is fine
    class ElderChild(Parent, typ="mine"):
        pass

    # Mapping transferred
    assert DictSerializable.class_mapping["mine"] is ElderChild

    with pytest.raises(ValueError, match="mine"):
        class SecondChild(Parent, typ="mine"):
            pass
