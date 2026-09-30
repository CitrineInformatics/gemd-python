"""Tests of the ingredient run object."""

import pytest

from gemd.entity.bounds.real_bounds import RealBounds
from gemd.entity.object.ingredient_run import IngredientRun
from gemd.entity.object.process_run import ProcessRun


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
        IngredientRun(material=RealBounds(0, 5.0, ""))
    with pytest.raises(TypeError):
        IngredientRun(process="process")
    with pytest.raises(TypeError):
        IngredientRun(spec=5)
    with pytest.raises(TypeError):
        IngredientRun(name=5)
    with pytest.raises(TypeError):
        IngredientRun(labels=[5])


def test_name_persistence():
    """Verify that a serialized IngredientRun doesn't lose its name."""
    from gemd.entity.link_by_uid import LinkByUID
    from gemd.entity.object import IngredientSpec
    from gemd.json import GEMDJson

    je = GEMDJson()

    ms_link = LinkByUID(scope="local", id="mat_spec")
    mr_link = LinkByUID(scope="local", id="mat_run")
    ps_link = LinkByUID(scope="local", id="pro_spec")
    pr_link = LinkByUID(scope="local", id="pro_run")
    spec = IngredientSpec(
        name="Ingred", labels=["some", "words"], process=ps_link, material=ms_link
    )
    run = IngredientRun(spec=spec, process=pr_link, material=mr_link)
    assert run.name == spec.name
    assert run.labels == spec.labels

    # Try changing them and make sure they change
    spec.name = "Frank"
    spec.labels = ["other", "words"]
    assert run.name == spec.name
    assert run.labels == spec.labels

    run.spec = LinkByUID(scope="local", id="ing_spec")
    # Name and labels are now stashed but not stored
    assert run == je.copy(run)
    assert run.name == spec.name
    assert run.labels == spec.labels

    # The stashed values are now the run's own, so a later spec does not replace them
    spec_too = IngredientSpec(name="Jorge", labels=[], process=ps_link, material=ms_link)
    run.spec = spec_too
    assert run == je.copy(run)
    assert run.name == spec.name
    assert run.labels == spec.labels


def test_own_name_and_labels():
    """The run's own name and labels take precedence over the spec's."""
    from gemd.entity.link_by_uid import LinkByUID
    from gemd.entity.object import IngredientSpec

    spec = IngredientSpec(name="Spec name", labels=["spec label"])

    # No values of its own and no spec
    run = IngredientRun()
    assert run.name is None
    assert run.labels == []

    # No values of its own: the spec's values show through
    run = IngredientRun(spec=spec)
    assert run.name == spec.name
    assert run.labels == spec.labels

    # Own values win, whether set in the constructor or later
    run = IngredientRun(name="Run name", labels=["run label"], spec=spec)
    assert run.name == "Run name"
    assert run.labels == ["run label"]

    run = IngredientRun(spec=spec)
    run.name = "Set later"
    run.labels = ["later label"]
    assert run.name == "Set later"
    assert run.labels == ["later label"]

    # Own values stay when the spec goes away
    run.spec = LinkByUID(scope="local", id="spec")
    assert run.name == "Set later"
    assert run.labels == ["later label"]

    # Clearing the own values restores the fallback
    run.spec = spec
    run.name = None
    run.labels = []
    assert run.name == spec.name
    assert run.labels == spec.labels


def test_name_and_labels_round_trip():
    """Own name and labels survive dict and json round trips."""
    from gemd.entity.object import IngredientSpec
    from gemd.json import dumps, loads

    spec = IngredientSpec(name="Spec name", labels=["spec label"])
    run = IngredientRun(name="Run name", labels=["run label"], spec=spec)

    as_dict = run.as_dict()
    assert as_dict["name"] == "Run name"
    assert as_dict["labels"] == ["run label"]
    assert "template" not in as_dict

    rebuilt = IngredientRun.from_dict(as_dict)
    assert rebuilt.name == "Run name"
    assert rebuilt.labels == ["run label"]

    copied = loads(dumps(run))
    assert copied.name == "Run name"
    assert copied.labels == ["run label"]
    assert copied.spec.name == spec.name

    # A run with no template link of its own
    with pytest.raises(AttributeError):
        run.template = None
