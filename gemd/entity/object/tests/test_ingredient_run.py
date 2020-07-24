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


def test_name_persistance():
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
    run.spec = LinkByUID(scope='local', id='ing_spec')
    # Name and labels are now stashed but not stored
    assert run == je.copy(run)
    assert run.name == spec.name
    assert run.labels == spec.labels


@pytest.mark.filterwarnings("ignore:Name is set implicitly")
@pytest.mark.filterwarnings("ignore:Labels are set implicitly")
@pytest.mark.filterwarnings("ignore:labels is deprecated")
def test_deprecated():
    """These are tests that will be obsolete but are required for 100 %."""
    name = 'name'
    labels = ['label', 'also']
    with pytest.raises(TypeError):
        IngredientRun(name=name)
    with pytest.raises(TypeError):
        IngredientRun(labels=labels)

    run = IngredientRun()
    run.name = name
    run.labels = labels
    assert run.name == name
    assert run.labels == labels
