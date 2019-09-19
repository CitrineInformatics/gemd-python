"""Test CompositionBounds."""
import pytest

from taurus.client.json_encoder import dumps, loads
from taurus.entity.bounds.composition_bounds import CompositionBounds
from taurus.entity.bounds.real_bounds import RealBounds
from taurus.entity.value.nominal_composition import NominalComposition
from taurus.entity.value.nominal_real import NominalReal
from taurus.entity.util import array_like


def test_components():
    """Test components setter."""
    assert CompositionBounds().components == set()
    assert CompositionBounds(components={"foo", "bar"}).components == {"foo", "bar"}
    assert CompositionBounds(components=["foo", "bar"]).components == {"foo", "bar"}


def test_invalid_constructor():
    """Test types in constructor."""
    with pytest.raises(ValueError):
        CompositionBounds(components="foo")

    with pytest.raises(ValueError):
        CompositionBounds(components={1, 2})


def test_contains():
    """Test basic contains logic."""
    bounds = CompositionBounds(components={"spam", "eggs"})
    assert bounds.contains(CompositionBounds(components={"spam"}))
    assert not bounds.contains(CompositionBounds(components={"foo"}))
    assert not bounds.contains(RealBounds(0.0, 2.0, ''))
    with pytest.raises(TypeError):
        bounds.contains({"spam"})


def test_json():
    """Test serialization (components is encoded as a list)."""
    bounds = CompositionBounds(components={"spam", "eggs"})
    copy = loads(dumps(bounds))
    assert copy == bounds


def test_numpy():
    """Test that ndarrays, Series work as well."""
    assert len(array_like()) < 5  # In case we extend at some point

    if len(array_like()) > 2:  # Test numpy
        import numpy as np

        np_bounds = CompositionBounds(components=np.array(["spam", "eggs"], dtype=object))
        np_copy = loads(dumps(np_bounds))
        assert np_copy == np_bounds

    if len(array_like()) > 3:  # Test pandas
        import pandas as pd

        pd_bounds = CompositionBounds(components=pd.Series(["spam", "eggs"]))
        pd_copy = loads(dumps(pd_bounds))
        assert pd_copy == pd_bounds
