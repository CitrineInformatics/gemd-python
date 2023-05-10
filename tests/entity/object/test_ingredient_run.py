"""Tests of the ingredient run object."""
import pytest

from gemd.entity.object.ingredient_run import IngredientRun
from gemd.entity.object.process_run import ProcessRun
from gemd.entity.bounds.real_bounds import RealBounds


def test_ingredient_reassignment():
    """Check that an ingredient run can be re-assigned to a new process run."""
    boiling = ProcessRun("Boil potatoes")
    frying = ProcessRun("Fry potatoes")
    oil = IngredientRun(process=boiling)
    potatoes = IngredientRun(process=boiling)
    assert oil.process == boiling
    assert set(boiling.ingredients) == {oil, potatoes}
    assert frying.ingredients == []

    oil.process = frying
    assert oil.process == frying
    assert boiling.ingredients == [potatoes]
    assert frying.ingredients == [oil]

    potatoes.process = frying
    assert potatoes.process == frying
    assert boiling.ingredients == []
    assert set(frying.ingredients) == {oil, potatoes}


def test_invalid_assignment():
    """Invalid assignments to `process` or `material` throw a TypeError."""
    with pytest.raises(TypeError):
        IngredientRun(material=RealBounds(0, 5.0, ''))
    with pytest.raises(TypeError):
        IngredientRun(process="process")
    with pytest.raises(TypeError):
        IngredientRun(spec=5)
    with pytest.raises(TypeError):
        IngredientRun(name="Flour")  # IngredientRuns don't have their own name


def test_name_persistence():
    """Verify that a serialized IngredientRun doesn't lose its name."""
    from gemd.entity.object import IngredientSpec
    from gemd.entity.link_by_uid import LinkByUID
    from gemd.json import GEMDJson

    je = GEMDJson()

    ms_link = LinkByUID(scope='local', id='mat_spec')
    mr_link = LinkByUID(scope='local', id='mat_run')
    ps_link = LinkByUID(scope='local', id='pro_spec')
    pr_link = LinkByUID(scope='local', id='pro_run')
    spec = IngredientSpec(name='Ingred', labels=['some', 'words'],
                          process=ps_link, material=ms_link)
    run = IngredientRun(spec=spec,
                        process=pr_link, material=mr_link)
    assert run.name == spec.name
    assert run.labels == spec.labels

    # Try changing them and make sure they change
    spec.name = 'Frank'
    spec.labels = ['other', 'words']
    assert run.name == spec.name
    assert run.labels == spec.labels

    run.spec = LinkByUID(scope='local', id='ing_spec')
    # Name and labels are now stashed but not stored
    assert run == je.copy(run)
    assert run.name == spec.name
    assert run.labels == spec.labels

    # Test that serialization doesn't get confused after a deser and set
    spec_too = IngredientSpec(name='Jorge', labels=[],
                              process=ps_link, material=ms_link)
    run.spec = spec_too
    assert run == je.copy(run)
    assert run.name == spec_too.name
    assert run.labels == spec_too.labels


def test_implicit_fields():
    """These test that users can't directly set names and labels."""
    name = 'name'
    labels = ['label', 'also']
    with pytest.raises(TypeError):
        IngredientRun(name=name)
    with pytest.raises(TypeError):
        IngredientRun(labels=labels)

    run = IngredientRun()
    with pytest.raises(AttributeError):
        run.name = name
    with pytest.raises(AttributeError):
        run.labels = labels
