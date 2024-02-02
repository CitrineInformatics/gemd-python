"""Test of CategoricalBounds."""
import pytest

from gemd.json import dumps, loads
from gemd.entity.bounds.categorical_bounds import CategoricalBounds
from gemd.entity.bounds.real_bounds import RealBounds
from gemd.entity.util import array_like
from gemd.entity.value.nominal_categorical import NominalCategorical


def test_categories():
    """Test categories setter."""
    assert CategoricalBounds().categories == set()
    assert CategoricalBounds(categories={"foo", "bar"}).categories == {"foo", "bar"}
    assert CategoricalBounds(categories=["foo", "bar"]).categories == {"foo", "bar"}


def test_invalid_constructor():
    """Test types for constructor."""
    with pytest.raises(ValueError):
        CategoricalBounds(categories="foo")

    with pytest.raises(ValueError):
        CategoricalBounds(categories={1, 2})


def test_contains():
    """Test basic contains logic."""
    bounds = CategoricalBounds(categories={"spam", "eggs"})
    assert bounds.contains(CategoricalBounds(categories={"spam"}))
    assert not bounds.contains(CategoricalBounds(categories={"spam", "foo"}))
    assert not bounds.contains(RealBounds(0.0, 2.0, ''))
    assert not bounds.contains(None)
    with pytest.raises(TypeError):
        bounds.contains({"spam", "eggs"})

    assert bounds.contains(NominalCategorical("spam"))
    assert not bounds.contains(NominalCategorical("foo"))


def test_union():
    """Test basic union & update logic."""
    bounds = CategoricalBounds(categories={"spam", "eggs"})
    value = NominalCategorical("cheese")
    assert bounds.union(value).contains(value), "Bounds didn't get new value"
    assert bounds.union(value).contains(bounds), "Bounds didn't keep old values"
    assert not bounds.contains(value), "Bounds got updated"

    bounds.update(value)
    assert bounds.contains(value), "Bounds didn't get updated"

    with pytest.raises(TypeError):
        bounds.union(RealBounds(0, 1, ""))


def test_json():
    """Test that serialization works (categories is encoded as a list)."""
    bounds = CategoricalBounds(categories={"spam", "eggs"})
    copy = loads(dumps(bounds))
    assert copy == bounds


def test_numpy():
    """Test that ndarrays, Series work as well."""
    assert len(array_like()) < 5  # In case we extend at some point

    if len(array_like()) > 2:  # Test numpy
        import numpy as np
        np_bounds = CategoricalBounds(np.array(["spam", "eggs"], dtype=object))
        np_copy = loads(dumps(np_bounds))
        assert np_copy == np_bounds

    if len(array_like()) > 3:  # Test pandas
        import pandas as pd
        pd_bounds = CategoricalBounds(pd.Series(["spam", "eggs"]))
        pd_copy = loads(dumps(pd_bounds))
        assert pd_copy == pd_bounds
